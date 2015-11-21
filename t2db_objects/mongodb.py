from pymongo import MongoClient
from bson.objectid import ObjectId

""" MONGO DB """
def getConnection(uri, dbName, clName):
  return MongoDB(uri).getDatabase(dbName).getCollection(clName)

class CollectionMongoDB(object):
  def __init__(self, database, name):
    if not type(database) is DatabaseMongoDB:
      raise Exception("Error, database is not Databasee type, found: ", type(database))
    self.collection = database.database[name]
  
  def getDoc(self, objectId):
    if not type(objectId) is int and not type(objectId) is ObjectId:
      raise Exception("Error, objectId is not int or ObjectId type, found: ", type(objectId))
    return self.collection.find_one({"_id" : objectId})
    
  def addDoc(self, document):
    if not type(document) is dict:
      raise Exception("Error, document is not Dict type, found: ", type(document))
    return self.collection.insert_one(document)

  def remDoc(self, objectId):
    if not type(objectId) is ObjectId:
      raise Exception("Error, objectId is not ObjectId type, found: ", type(objectId))
    return self.collection.delete_one({"_id" : objectId})

  def updDoc(self, document):
    if not type(document) is dict:
      raise Exception("Error, document is not dict type, found: ", type(document))
    return self.collection.replace_one({"_id": document["_id"]}, document)

  def remDocByCriteria(self, criteria):
    if not type(criteria) is dict:
      raise Exception("Error, criteria is not dict type, found: ", type(criteria))
    return self.collection.delete_many(criteria)

  def updDocByCriteria(self, criteria, newValues):
    if not type(criteria) is dict:
      raise Exception("Error, criteria is not dict type, found: ", type(criteria))
    if not type(newValues) is dict:
      raise Exception("Error, newValues is not dict type, found: ", type(newValues))
    return self.collection.update_many(criteria, {"$set": newValues})

  def addManyDocs(self, documents):
    if not type(documents) is list:
      raise Exception("Error, documents is not list, found: ", type(documents))
    return self.collection.insert_many(documents)

  def getDocByCriteria(self, criteria):
    if not type(criteria) is dict:
      raise Exception("Error, criteria is not list dict, found: ", type(criteria))
    result = []
    for doc in self.collection.find(criteria):
      result.append(doc)
    return result

  def remAll(self):
    return self.collection.delete_many({})

class DatabaseMongoDB(object):
  def __init__(self, mongoDB, name):
    if not type(mongoDB) is MongoDB:
      raise Exception("Error, mongoDB is not MongoDB type, found: ", type(mongoDB))
    self.database = mongoDB.client[name]
    
  def getCollection(self, name):
    return CollectionMongoDB(self, name)

class MongoDB(object):
  def __init__(self, uri, **kwargs):
    try:
      self.client = MongoClient(uri, **kwargs)
    except Exception as e:
      raise
    if not self.client.server_info():
      raise("Error: Mongodb communication failed")
  
  def close(self):
    self.client.close()
    
  def getDatabase(self, name):
    return DatabaseMongoDB(self, name)
    
