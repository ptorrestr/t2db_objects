#!/usr/bin/env python3
# objects.py tests

import unittest
import random
import string

from t2db_objects.objects import User
from t2db_objects.objects import Tweet
from t2db_objects.objects import Job
from t2db_objects.objects import Configuration
from t2db_objects.objects import ObjectList
from t2db_objects.objects import parseText
from t2db_objects.objects import encodeObject
from t2db_objects.objects import formatHash

from t2db_objects.utilities import readConfigFile
from t2db_objects.utilities import writeFile
from t2db_objects.utilities import removeFile

from t2db_objects.tests.common import randomInteger
from t2db_objects.tests.common import randomBoolean
from t2db_objects.tests.common import randomStringFixed
from t2db_objects.tests.common import randomStringVariable
from t2db_objects.tests.common import randomText
from t2db_objects.tests.common import randomUrl
from t2db_objects.tests.common import randomTweet
from t2db_objects.tests.common import randomUser
from t2db_objects.tests.common import randomJob


###############################################################################
# Test for TWEET object
#
###############################################################################
class TestTweetObject(unittest.TestCase):
    def setUp(self):
        self.rawTweet0 = randomTweet(0, "date", 0)
        self.rawTweet1 = randomTweet(1, "date", 0)
        #Invalid tweet no id
        self.rawTweet2 = randomTweet(2, "date", 0)
        del self.rawTweet2["id"]
        #Invalid tweet, no created_at
        self.rawTweet3 = randomTweet(3, "date", 0)
        del self.rawTweet3["created_at"]
        #Invalid tweet, no user
        self.rawTweet4 = randomTweet(4, "date", 0)
        del self.rawTweet4["user"]

    def test_tweetCreationValid(self):
        tweet0 = Tweet(self.rawTweet0)
        tweet1 = Tweet(self.rawTweet1)
        self.assertTrue(tweet0.equalHash(self.rawTweet0))
        self.assertTrue(tweet1.equalHash(self.rawTweet1))

    def test_tweetCompareTo(self):
        tweet0 = Tweet(self.rawTweet0)
        tweet1 = Tweet(self.rawTweet1)
        self.assertTrue(tweet0.equal(tweet0))
        self.assertFalse(tweet0.equal(tweet1))

    def test_tweetCreationInvalid(self):
        self.assertRaises(Exception, Tweet, self.rawTweet2)
        self.assertRaises(Exception, Tweet, self.rawTweet3)
        self.assertRaises(Exception, Tweet, self.rawTweet4)

    def test_tweetToHash(self):
        tweet0 = Tweet(self.rawTweet0)
        tweet1 = Tweet(self.rawTweet1)
        hashTweet1 = tweet1.toHash()
        hashTweet0 = tweet0.toHash()
        self.assertTrue(tweet0.equalHash(hashTweet0))
        self.assertTrue(tweet1.equalHash(hashTweet1))

###############################################################################
# Test for USER object
#
###############################################################################
class TestUserObject(unittest.TestCase):
    def setUp(self):
        self.rawUser0 = randomUser(0, "date", "user0")
        self.rawUser1 = randomUser(1, "date", "user1")
        # Invalid user no id
        self.rawUser2 = randomUser(2, "date", "user2")
        del self.rawUser2["id"]
        # Invalid user no created_at
        self.rawUser3 = randomUser(3, "date", "user3")
        del self.rawUser3["created_at"]
        # Invalid user no name
        self.rawUser4 = randomUser(4, "date", "user4")
        del self.rawUser4["name"]

    def test_userCreationValid(self):
        user0 = User(self.rawUser0)
        user1 = User(self.rawUser1)
        self.assertTrue(user0.equalHash(self.rawUser0))
        self.assertTrue(user1.equalHash(self.rawUser1))

    def test_userEqual(self):
        user0 = User(self.rawUser0)
        user1 = User(self.rawUser1)
        self.assertTrue(user0.equal(user0))
        self.assertFalse(user0.equal(user1))

    def test_userCreationInvalid(self):
        self.assertRaises(Exception, User, self.rawUser2)
        self.assertRaises(Exception, User, self.rawUser3)
        self.assertRaises(Exception, User, self.rawUser4)

    def test_userToHash(self):
        user0 = User(self.rawUser0)
        user1 = User(self.rawUser1)
        hashUser0 = user0.toHash()
        hashUser1 = user1.toHash()
        self.assertTrue(user0.equalHash(hashUser0))
        self.assertTrue(user1.equalHash(hashUser1))

###############################################################################
# test for JOB object
#
###############################################################################
class TestJobObject(unittest.TestCase):
    def setUp(self):
        self.rawJob0 = randomJob("START", 0)
        self.rawJob1 = randomJob("DELETE", 1)
        #Invalid user no command
        self.rawJob2 = randomJob("START", 2)
        del self.rawJob2["command"]
        #Invalid user no process_id
        self.rawJob3 = randomJob("DELETE", 3)
        del self.rawJob3["process_id"]

    def test_jobCreationValid(self):
        job0 = Job(self.rawJob0)
        job1 = Job(self.rawJob1)
        self.assertTrue(job0.equalHash(self.rawJob0))
        self.assertTrue(job1.equalHash(self.rawJob1))

    def test_jobEqual(self):
        job0 = Job(self.rawJob0)
        job1 = Job(self.rawJob1)
        self.assertTrue(job0.equal(job0))
        self.assertFalse(job0.equal(job1))

    def test_jobCreationInvalid(self):
        self.assertRaises(Exception, Job, self.rawJob2)
        self.assertRaises(Exception, Job, self.rawJob3)

    def test_jobToHash(self):
        job0 = Job(self.rawJob0)
        job1 = Job(self.rawJob1)
        hashJob0 = job0.toHash()
        hashJob1 = job1.toHash()
        self.assertTrue(job0.equalHash(hashJob0))
        self.assertTrue(job1.equalHash(hashJob1))

###############################################################################
# test for CONFIGURATION object
#
###############################################################################
class TestConfigurationObject(unittest.TestCase):
    def setUp(self):
        self.configFilePath = "./tempConfigFile.conf"
        self.configurationFields = [
            {"name":"urldatabase", "kind":"mandatory", "type":str},
            {"name":"socket_port", "kind":"mandatory", "type":int},
            {"name":"max_connection", "kind":"mandatory", "type":int},
            {"name":"collector_app", "kind":"mandatory", "type":str},
            {"name":"path_collector_app", "kind":"mandatory", "type":str},
            {"name":"output_folder", "kind":"mandatory", "type":str},
            ]

        # Create a temporal file with configuration
        outputStr = ""
        for field in self.configurationFields:
            if field["type"] == str:
                outputStr += field["name"] + " = " + randomStringFixed(10)
            elif field["type"] == int:
                outputStr += field["name"] + " = " + str(randomInteger(100))
            outputStr += "\n"
        writeFile(self.configFilePath, outputStr)

    def test_configurationCreationValid(self):
        rawConfigurationNoFormat = readConfigFile(self.configFilePath)
        rawConfiguration = formatHash(rawConfigurationNoFormat, self.configurationFields)
        configuration = Configuration(self.configurationFields, rawConfiguration)
        self.assertTrue(configuration, rawConfiguration)

    def test_configurationCreationInvalid(self):
        rawConfigurationNoFormat = readConfigFile(self.configFilePath)
        rawConfiguration = formatHash(rawConfigurationNoFormat, self.configurationFields)
        del rawConfiguration["urldatabase"]
        self.assertRaises(Exception, Configuration, (self.configurationFields, rawConfiguration))

    def tearDown(self):
        removeFile(self.configFilePath)

###############################################################################
# Test for OBJECTLIST object
#
###############################################################################
class TestObjectList(unittest.TestCase):
    def setUp(self):
        self.rawTweet0 = randomTweet(0, "date", 0)
        self.rawTweet1 = randomTweet(0, "date", 1)
        self.rawUser0 = randomUser(0, "date", "user0")
        self.rawUser1 = randomUser(1, "date", "user1")

    def test_listAppendValid(self):
        randomElements = randomInteger(100)
        objectList1 = ObjectList()
        for i in range(0,randomElements):
            tweet = Tweet(randomTweet(i,"date", 0))
            objectList1.append(tweet)
            self.assertTrue( (i + 1) == len(objectList1.getList()))
        self.assertTrue( randomElements == len(objectList1.getList()))

    def test_listAppendInvalid(self):
        randomElements = randomInteger(100)
        objectList1 = ObjectList()
        for i in range(0, randomElements):
            map0 = {}
            self.assertRaises(Exception, ObjectList.append, map0)

    def test_listToHash(self):
        randomElements = randomInteger(100)
        objectList1 = ObjectList()
        for i in range(0, randomElements):
            tweet = Tweet(randomTweet(i, "date", 0))
            objectList1.append(tweet)
        hashObjectList1 = objectList1.toHash()
        internalList1 = objectList1.getList()
        self.assertTrue("list" in hashObjectList1)
        for i in range(0, randomElements):
            subHash = hashObjectList1["list"][i]
            self.assertTrue(internalList1[i].equalHash(subHash))

    def test_listParse(self):
        randomElements = randomInteger(100)
        objectList1 = ObjectList()
        for i in range(0, randomElements):
            tweet = Tweet(randomTweet(i, "date", 0))
            objectList1.append(tweet)
        hashObjectList1 = objectList1.toHash()
        parsedObjectList1 = ObjectList()
        parsedObjectList1.parse(hashObjectList1)
        internalList1 = objectList1.getList()
        internalList2 = parsedObjectList1.getList()
        for i in range(0, randomElements):
            self.assertTrue(internalList1[i].equal(internalList2[i]))

###############################################################################
# Test for PARSETEXT and ENCODEOBJECT methods
#
###############################################################################

class TestParseEncodeMethods(unittest.TestCase):
    def test_parseEncodeTweet(self):
        randomElements = randomInteger(100)
        for i in range(0, randomElements):
            tweet1 = Tweet(randomTweet(i, "date", 0))
            encodeTweet1 = encodeObject(tweet1)
            tweet2 = parseText(encodeTweet1)
            self.assertTrue(tweet1.equal(tweet2))

    def test_parseEncodeUser(self):
        randomElements = randomInteger(100)
        for i in range(0, randomElements):
            user1 = User(randomUser(i, "date", "user1"))
            encodeUser1 = encodeObject(user1)
            user2 = parseText(encodeUser1)
            self.assertTrue(user1.equal(user2))

    def test_parseEncodeJob(self):
        randomElements = randomInteger(100)
        for i in range(0, randomElements):
            job1 = Job(randomJob("START", i))
            encodeJob1 = encodeObject(job1)
            job2 = parseText(encodeJob1)
            self.assertTrue(job1.equal(job2))

    def test_parseEncodeObjectList(self):
        randomObjectElements = randomInteger(100)
        for j in range(0, randomObjectElements):
            randomElements = randomInteger(100)
            objectList1 = ObjectList()
            for i in range(0, randomElements):
                tweet = Tweet(randomTweet(i, "date", 0))
                objectList1.append(tweet)
            encodeObjectList1 = encodeObject(objectList1)
            objectList2 = parseText(encodeObjectList1)
            internalList1 = objectList1.getList()
            internalList2 = objectList2.getList()
            for i in range(0, randomElements):
                self.assertTrue(internalList1[i].equal(internalList2[i]))

