import unittest

from t2db_objects.mongodb import CollectionMongoDB
from t2db_objects.mongodb import DatabaseMongoDB
from t2db_objects.mongodb import MongoDB

class TestCollectionMongoDB(unittest.TestCase):
  def setUp(self):
    connection = MongoDB("localhost")
    self.db = DatabaseMongoDB(connection, "name")

  def test_validCreation(self):
    collection = CollectionMongoDB(self.db, "name")

  def test_notValidCreation(self):
    self.assertRaises(Exception, CollectionMongoDB, (None, "name",))

  def test_addGetRemUpdDoc(self):
    collection = CollectionMongoDB(self.db, "name")
    testDocument = { "value1": 123, "value2": 321 }
    id1 = collection.addDoc(testDocument)
    storedDocument = collection.getDoc(id1)
    self.assertEqual(testDocument["value1"], storedDocument["value1"])
    self.assertEqual(testDocument["value2"], storedDocument["value2"])
    storedDocument["value1"] = 456
    storedDocument["value2"] = 654
    res = collection.updDoc(storedDocument)
    self.assertEqual(res["n"], 1)
    res = collection.remDoc(id1)
    self.assertEqual(res["n"], 1)

  def test_notValidAddDoc(self):
    collection = CollectionMongoDB(self.db, "name")
    self.assertRaises(Exception, collection.addDoc, (123,))

  def test_notValidGetDoc(self):
    collection = CollectionMongoDB(self.db, "name")
    self.assertRaises(Exception, collection.getDoc, (123,))

  def test_notValidRemDoc(self):
    collection = CollectionMongoDB(self.db, "name")
    self.assertRaises(Exception, collection.remDoc, (123,))

  def test_notValidUpdDoc(self):
    collection = CollectionMongoDB(self.db, "name")
    self.assertRaises(Exception, collection.updDoc, (123,))

  def test_remDocByCriteria(self):
    collection = CollectionMongoDB(self.db, "name")
    document1 = { "value1": 123, "value2": 321 }
    document2 = { "value1": 123, "value2": 456 }
    docs =[ document1, document2 ]
    [id1, id2] = collection.addManyDocs(docs)
    stored1 = collection.getDoc(id1)
    stored2 = collection.getDoc(id2)
    self.assertEqual(document1["value1"], stored1["value1"])
    self.assertEqual(document1["value2"], stored1["value2"])
    self.assertEqual(document2["value1"], stored2["value1"])
    self.assertEqual(document2["value2"], stored2["value2"])
    criteria = {"value1":document1["value1"]}
    res = collection.remDocByCriteria(criteria)
    self.assertGreater(res["n"], 1)
    id1 = collection.addDoc(document1)
    id2 = collection.addDoc(document2)
    criteria = {"value2":document1["value2"]}
    res = collection.remDocByCriteria(criteria)
    self.assertEqual(res["n"], 1)
    stored2 = collection.getDoc(id2)
    self.assertEqual(document2["value1"], stored2["value1"])
    self.assertEqual(document2["value2"], stored2["value2"])
    collection.remAll()

  def test_notValidRemDocByCriteria(self):
    collection = CollectionMongoDB(self.db, "name")
    criteria = "wrong criteria"
    self.assertRaises(Exception, collection.remDocByCriteria, (criteria,))

  def test_updDocByCriteria(self):
    collection = CollectionMongoDB(self.db, "name")
    document1 = { "value1": 123, "value2": 321 }
    document2 = { "value1": 123, "value2": 456 }
    docs =[ document1, document2 ]
    [id1, id2] = collection.addManyDocs(docs)
    stored1 = collection.getDoc(id1)
    stored2 = collection.getDoc(id2)
    self.assertEqual(document1["value1"], stored1["value1"])
    self.assertEqual(document1["value2"], stored1["value2"])
    self.assertEqual(document2["value1"], stored2["value1"])
    self.assertEqual(document2["value2"], stored2["value2"])
    criteria = { "value1":document1["value1"] }
    newValues = { "value1": 1 }
    res = collection.updDocByCriteria(criteria, newValues)
    self.assertEqual(res["n"], 2)
    criteria = { "value2":document1["value2"] }
    newValues = { "value2": 2 }
    res = collection.updDocByCriteria(criteria, newValues)
    self.assertEqual(res["n"], 1)
    criteria = { "value1" : 1 }
    res = collection.remDocByCriteria(criteria)
    self.assertEqual(res["n"], 2)

  def test_notValidUpdDocByCriteria(self):
    collection = CollectionMongoDB(self.db, "name")
    criteria = { "value1": 1 }
    newValues = { "value1": 2 }
    notValid_criteria = "wrong criteria"
    notValid_newValues = "wrong values"
    self.assertRaises(Exception, collection.updDocByCriteria, (criteria, notValid_newValues,))
    self.assertRaises(Exception, collection.updDocByCriteria, (notValid_criteria, newValues,))

  def test_addManyDocs(self):
    collection = CollectionMongoDB(self.db, "name")
    docs = [ { "id":90, "value":10}, {"value1":90, "value2":11 } ]
    [id1, id2 ] = collection.addManyDocs(docs)
    collection.remAll()

  def test_getDocByCriteria(self):
    collection = CollectionMongoDB(self.db, "name")
    docs = [ {"value1":90, "value2":10}, { "value1":90, "value2":11 } ]
    [id1, id2 ] = collection.addManyDocs(docs)
    criteria = { "value1":90 }
    storedDocs = collection.getDocByCriteria(criteria)
    self.assertEqual(len(storedDocs), 2)
    collection.remAll()

  def test_notValidGetDocByCriteria(self):
    collection = CollectionMongoDB(self.db, "name")
    criteria = "wrong criteria"
    self.assertRaises(Exception, collection.getDocByCriteria, (criteria,))

class TestDatabaseMongoDB(unittest.TestCase):
  def test_validCreation(self):
    connection = MongoDB("localhost")
    db = DatabaseMongoDB(connection, "name")

  def test_notValidCreation(self):
    self.assertRaises(Exception, DatabaseMongoDB, (None, "name",))

  def test_getCollection(self):
    connection = MongoDB("localhost")
    db = DatabaseMongoDB(connection, "name")
    collection = db.getCollection("name")

class TestMonogDB(unittest.TestCase):
  def test_validCreation(self):
    connection = MongoDB("localhost")
    
  def test_notValidCreation(self):
    self.assertRaises(Exception, MongoDB, ("otherHost",))

  def test_close(self):
    connection = MongoDB("localhost")
    connection.close()

  def test_getDatabase(self):
    connection = MongoDB("localhost")
    connection.getDatabase("name")
