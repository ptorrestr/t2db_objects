import json
from .utilities import boolean2int
#TODO Get automatically data model from webservice

# Return the json representation of the dataObject in string format. If 
# encoding fails, an exception is raised describing the error, otherwise 
# return a json string.
def encodeObject(dataObject):
    if not "toHash" in dir(dataObject):
        raise Exception ("No toHash method found in dataObject")
    hashObject = dataObject.toHash()
    return json.dumps(hashObject)

# Return the valid object described by dataText. DataText is a json string
# If parsing fails, an exception is raised, otherwise return the 
# appropiate object.
def parseText(dataText):
    if type(dataText) is not str:
        raise Exception ("DataText is not string object, cannot parse it")
    rawObject = json.loads(dataText)
    if type(rawObject) is not dict:
        raise Exception ("RawObject is not dictionary. Parsing failed")
    if not "_type" in rawObject:
        raise Exception ("RawObject does not have _type attribute. Parsing failed")
    if rawObject["_type"] == "Tweet":
        return Tweet(rawObject)
    elif rawObject["_type"] == "User":
        return User(rawObject)
    elif rawObject["_type"] == "TweetStreaming":
        return TweetStreaming(rawObject)
    elif rawObject["_type"] == "TweetSearch":
        return TweetSearch(rawObject)
    elif rawObject["_type"] == "Job":
        return Job(rawObject)
    elif rawObject["_type"] == "ObjectList":
        objectList = ObjectList()
        objectList.parse(rawObject)
        return objectList
    else:
        raise Exception ("Invalid type. Parsing failed")

#Store only objects with toHash function
class ObjectList(object):
    def __init__(self):
        self.list = []

    # Store object element in list only if element has toHash function
    def append(self, element):
        if not "toHash" in dir(element):
            raise Exception ("Element does not have toHash function")
        self.list.append(element)

    # Get the object list
    def getList(self):
        return self.list

    # Generate a hash representation of the object
    def toHash(self):
        hashList = {}
        hashList["_type"] = "ObjectList"
        rawList = []
        for element in self.list:
            rawList.append(element.toHash())
        hashList["list"] = rawList
        return hashList

    def parse(self, rawObjectList):
        if not "list" in rawObjectList:
            raise Exception ("RawObjectList does not have list, discarding")
        for hashElement in rawObjectList["list"]:
            if not "_type" in hashElement:
                raise Exception ("No _type found")
            type_ = hashElement["_type"]
            if type_ == "User":
                self.list.append(User(hashElement))
            elif type_ == "Tweet":
                self.list.append(Tweet(hashElement))
            elif type_ == "Job":
                self.list.append(Job(hashElement))
            else:
                raise Exception ("Type '" + str(type_) + "' is not valid")

tweetFields = [
        {"name":"id","kind":"mandatory","type":int},
        {"name":"retweet_count", "kind":"non-mandatory", "type":int},
        {"name":"created_at", "kind":"mandatory", "type":str},
        {"name":"text", "kind":"non-mandatory", "type":str},
        {"name":"in_reply_to_screen_name", "kind":"non-mandatory", "type":str},
        {"name":"in_reply_to_user_id", "kind":"non-mandatory", "type":int},
        {"name":"in_reply_to_status_id", "kind":"non-mandatory", "type":int},
        {"name":"source", "kind":"non-mandatory", "type":str},
        {"name":"urls", "kind":"non-mandatory", "type":str},
        {"name":"user_mentions", "kind":"non-mandatory", "type":str}, 
        {"name":"hashtags", "kind":"non-mandatory", "type":str},
        #{"name":"geo", "kind":"non-mandatory", "type":str}, #deprecated
        {"name":"place", "kind":"non-mandatory", "type":str},
        {"name":"coordinates", "kind":"non-mandatory", "type":str},
        {"name":"contributors", "kind":"non-mandatory", "type":str},
        {"name":"favorited", "kind":"non-mandatory", "type":bool},
        {"name":"truncated", "kind":"non-mandatory", "type":bool},
        {"name":"retweeted", "kind":"non-mandatory", "type":bool},
        {"name":"user", "kind":"mandatory", "type":int},
        ]
        #ADD case for OBJECTS!
        #args['user'] = self.user.id

# Fields
userFields = [
        {"name":"id","kind": "mandatory", "type":int},
        {"name":"utc_offset", "kind":"non-mandatory", "type":int},
        {"name":"followers_count", "kind":"non-mandatory", "type":int},
        {"name":"friends_count","kind":"non-mandatory", "type":int}, 
        {"name":"statuses_count","kind":"non-mandatory", "type":int},
        {"name":"favourites_count", "kind":"non-mandatory", "type":int},
        {"name":"listed_count", "kind":"non-mandatory", "type":int},
        {"name":"created_at","kind":"mandatory", "type":str},
        {"name":"name", "kind":"mandatory", "type":str},
        {"name":"screen_name","kind":"non-mandatory", "type":str}, 
        {"name":"location", "kind":"non-mandatory", "type":str}, 
        {"name":"description", "kind":"non-mandatory", "type":str},
        {"name":"profile_image_url", "kind":"non-mandatory", "type":str},
        {"name":"profile_image_url_https", "kind":"non-mandatory", "type":str},
        {"name":"profile_background_image_url", "kind":"non-mandatory", "type":str},
        {"name":"profile_background_color", "kind":"non-mandatory", "type":str},
        {"name":"profile_sidebar_fill_color", "kind":"non-mandatory", "type":str},
        {"name":"profile_sidebar_border_color", "kind":"non-mandatory", "type":str},
        {"name":"profile_link_color", "kind":"non-mandatory", "type":str},
        {"name":"profile_text_color", "kind":"non-mandatory", "type":str},
        {"name":"time_zone", "kind":"non-mandatory","type":str},
        {"name":"url", "kind":"non-mandatory", "type":str},
        {"name":"lang", "kind":"non-mandatory", "type":str},
        {"name":"profile_background_tile", "kind":"non-mandatory", "type":bool},
        {"name":"protected", "kind":"non-mandatory", "type":bool},
        {"name":"geo_enabled", "kind":"non-mandatory", "type":bool},
        {"name":"verified", "kind":"non-mandatory", "type":bool},
        {"name":"notifications", "kind":"non-mandatory", "type":bool},
        {"name":"contributors_enabled", "kind":"non-mandatory", "type":bool},
        ]

# Fields for Job
jobFields = [
        {"name":"command", "kind":"mandatory", "type":str},
        {"name":"process_id", "kind":"mandatory", "type":int},
        {"name":"consumer", "kind":"non-mandatory", "type":str},
        {"name":"consumer_sec", "kind":"non-mandatory", "type":str},
        {"name":"access", "kind":"non-mandatory", "type":str},
        {"name":"access_sec", "kind":"non-mandatory", "type":str},
        {"name":"query", "kind":"non-mandatory", "type":str},
        {"name":"kind", "kind":"non-mandatory", "type":str},
        ]

# Fields for TweetStreaming
tweetStreamingFields = [
        {"name":"tweet", "kind":"mandatory", "type":int},
        {"name":"streaming", "kind":"mandatory", "type":int},
        ]

# Fields for TweetSearch
tweetSearchFields = [
        {"name":"tweet", "kind":"mandatory", "type":int},
        {"name":"search", "kind":"mandatory", "type":int},
        ]

class Object(object):
    # Base type for all object. The constructor automatically build an object
    # discribed by objectFields and add the data contained in rawObject. 
    # Biside, this object implement toHash function which transform the object
    # to a hashMap
    def __init__(self, objectFields, rawObject):
        for field in objectFields:
            if not "name" in field:
                raise Exception ("'" + field + "' is not valid tuple: Name missing")
            if not "kind" in field:
                raise Exception ("'" + field + "' is not valid tuple: Kind missing")
            if not "type" in field:
                raise Exception ("'" + field + "' is not valid tuple: Type missing")
            name_ = field["name"]
            kind_ = field["kind"]
            type_ = field["type"]
            if kind_ == "mandatory":
                if not name_ in rawObject:
                    raise Exception ("RawObject does not have '" + name_ + "'")
                myType = type(rawObject[name_])
                if myType is not type_ and myType is not type(None):
                    raise Exception ("'"+ name_ + "' must be '" + str(type_) + "'")
                self.__dict__[name_] = rawObject[name_]
            elif kind_ == "non-mandatory":
                if not name_ in rawObject:
                    self.__dict__[name_] = None
                else:
                    myType = type(rawObject[name_])
                    if myType is not type_ and myType is not type(None):
                        raise Exception ("'"+ name_ + "' must be '" + str(type_) + "'")
                    self.__dict__[name_] = rawObject[name_]
        self.myFields = objectFields

    def toHash(self):
        args = {}
        for field in self.myFields:
            if not "name" in field:
                raise Exception ("'" + field + "' is not valid tuple")
            name_ = field["name"]
            if not name_ in self.__dict__:
                raise Exception ("'Object does not have '" + name_ + "'")
            args[name_] = self.__dict__[name_]
        return args

    def equal(self, rObject):
        hash_ = rObject.__dict__
        return self.equalHash(hash_)

    def equalHash(self, rHash):
        for field in self.myFields:
            if not "name" in field:
                raise Exception ("'" + field + "' is not valid tuple: Name missing")
            if not "kind" in field:
                raise Exception ("'" + field + "' is not valid tuple: Kind missing")
            if not "type" in field:
                raise Exception ("'" + field + "' is not valid tuple: Type missing")
            name_ = field["name"]
            kind_ = field["kind"]
            type_ = field["type"]
            # If field is mandatory and is not present in self
            if kind_ == "mandatory" and not name_ in self.__dict__:
                raise Exception ("'Left object does not have '" + name_ + "'")
            if kind_ == "mandatory" and not name_ in rHash:
                raise Exception ("'Rigth object does not have '" + name_ + "'")
            # If field in left object and not in right object?
            if name_ in self.__dict__ and not name_ in rHash:
                return False
            if name_ in rHash and not name_ in self.__dict__:
                return False
            if not self.__dict__[name_] == rHash[name_]:
                return False
        return True

# Format hash to corresponding type
def formatHash(myHash, myFields):
    newHash = {}
    for field in myFields:
        if not "name" in field:
            raise Exception ("'" + field + "' is not valid tuple: Name missing")
        if not "kind" in field:
            raise Exception ("'" + field + "' is not valid tuple: Kind missing")
        if not "type" in field:
            raise Exception ("'" + field + "' is not valid tuple: Type missing")
        name_ = field["name"]
        kind_ = field["kind"]
        type_ = field["type"]
        if kind_ == "mandatory" and not name_ in myHash:
            raise Exception ("'Object does not have '" + name_ + "'")
        if name_ in myHash:
            newHash[name_] = type_(myHash[name_])
    return newHash

class Tweet(Object):
    # Create a new tweet object. Use only the inputdata provided. If the data
    # is not given for a field, a None object is added in the field. Only
    # Mandatory data is foreced (id, created_at, user).
    def __init__(self, rawTweet):
        try:
            super(Tweet, self).__init__(tweetFields, rawTweet)
        except Exception as e:
            raise Exception("Tweet creation failed: " + str(e))

    def toHash(self):
        args = super(Tweet, self).toHash()
        args['_type'] = "Tweet"
        return args

    def equal(self, rObject):
        return super(Tweet, self).equal(rObject)

    def equalHash(self, rHash):
        return super(Tweet, self).equalHash(rHash)

class User(Object):
    # Create a new user object. Use only the inputdata provided. If the data
    # is not given for a field, a None object is added in the field. Only
    # Mandatory data is foreced (id, created_at, name).
    def __init__(self, rawUser):
        try:
            super(User, self).__init__(userFields, rawUser)
        except Exception as e:
            raise Exception("User creation failed: " + str(e))

    def toHash(self):
        args = super(User,self).toHash()
        args['_type'] = "User"
        return args

    def equal(self, rObject):
        return super(User, self).equal(rObject)

    def equalHash(self, rHash):
        return super(User, self).equalHash(rHash)

class Job(Object):
    # Create a new Job Object. If the data is not given for a field, a None
    # object is added in the field. Only mandatory data is forced (command,
    # process_id)
    def __init__(self, rawJob):
        try:
            super(Job, self).__init__(jobFields, rawJob)
        except Exception as e:
            raise Exception("Job creation failed: " + str(e))

    def toHash(self):
        args = super(Job, self).toHash()
        args['_type'] = "Job"
        return args

    def equal(self, rObject):
        return super(Job, self).equal(rObject)

    def equalHash(self, rHash):
        return super(Job, self).equalHash(rHash)

class TweetStreaming(Object):
    # Create a new TweetStreaming Object. If the data is not given for a field, 
    # a None object is added in the field. Only mandatory data is forced (tweet,
    # streaming)
    def __init__(self, rawTweetStreaming):
        try:
            super(TweetStreaming, self).__init__(tweetStreamingFields,
                rawTweetStreaming)
        except Exception as e:
            raise Exception("TweetStreaming creation failed: " + str(e))

    def toHash(self):
        args = super(TweetStreaming, self).toHash()
        args['_type'] = "TweetStreaming"
        return args

    def equal(self, rObject):
        return super(TweetStreaming, self).equal(rObject)

    def equalHash(self, rHash):
        return super(TweetStreaming, self).equalHash(rHash)

class TweetSearch(Object):
    # Create a new TweetSearch Object. If the data is not given for a field, 
    # a None object is added in the field. Only mandatory data is forced (tweet,
    # search)
    def __init__(self, rawTweetSearch):
        try:
            super(TweetSearch, self).__init__(tweetSearchFields, rawTweetSearch)
        except Exception as e:
            raise Exception("TweetSearch creation failed: " + str(e))

    def toHash(self):
        args = super(TweetSearch, self).toHash()
        args['_type'] = "TweetSearch"
        return args

    def equal(self, rObject):
        return super(TweetSearch, self).equal(rObject)

    def equalHash(self, rHash):
        return super(TweetSearch, self).equalHash(rHash)

class Configuration(Object):
    # This objects is for the input configuration given by the user through a
    # file. It works similar as every Object: The user must defined a model and
    # given to it in the constructor.

    def __init__(self, configurationFields, rawConfiguration):
        try:
            super(Configuration, self).__init__(configurationFields, rawConfiguration)
        except Exception as e:
            raise Exception("Configuration creation failed: " + str(e))
    
    def toHash(self):
        args = super(Configuration, self).toHash()
        args['_type'] = "Configuration"
        return args

    def equal(self, rObject):
        return super(Configuration, self).equal(rObject)

    def equalHash(self, rHash):
        return super(Configuration, self).equalHash(rHash)

# TODO this object is not used
class Entities(object):
    def __init__(self, rawEntities):
        self.urls = rawEntities['urls']
        self.hashtags = rawEntities['hashtags']
        self.user_mentions = rawEntities['user_mentions']

# TODO this object is not used
class Metadata(object):
    def __init__(self, rawMetadata):
        self.iso_language_code = rawMetadata['iso_language_code']
        self.result_type = rawMetadata['result_type']

