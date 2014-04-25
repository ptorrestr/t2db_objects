#!/usr/bin/env python3
# objects.py tests

import unittest
import random
import string

from t2db_objects.objects import User
from t2db_objects.objects import Tweet
from t2db_objects.objects import Job
from t2db_objects.objects import TweetStreaming
from t2db_objects.objects import TweetSearch
from t2db_objects.objects import Streaming
from t2db_objects.objects import Search
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
from t2db_objects.tests.common import randomTweetStreaming
from t2db_objects.tests.common import randomTweetSearch
from t2db_objects.tests.common import randomStreaming
from t2db_objects.tests.common import randomSearch

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

    def test_tweetWithNone(self):
        self.rawTweet0["text"] = None
        tweet0 = Tweet(self.rawTweet0)

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

    def test_userWithNone(self):
        self.rawUser0["created_at"] = None
        user0 = User(self.rawUser0)

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

    def test_jobWithNone(self):
        self.rawJob0["command"] = None
        job0 = Job(self.rawJob0)

###############################################################################
# test for TweetStreaming object
#
###############################################################################
class TestTweetStreamingObject(unittest.TestCase):
    def setUp(self):
        self.rawTweetStreaming0 = randomTweetStreaming(0, 0)
        self.rawTweetStreaming1 = randomTweetStreaming(1, 1)
        #Invalid TweetStreaming, no tweet
        self.rawTweetStreaming2 = randomTweetStreaming(2, 2)
        del self.rawTweetStreaming2["tweet"]
        #Invalid TweetStreaming, no streaming
        self.rawTweetStreaming3 = randomTweetStreaming(3, 3)
        del self.rawTweetStreaming3["streaming"]

    def test_tweetStreamingCreationValid(self):
        tweetStreaming0 = TweetStreaming(self.rawTweetStreaming0)
        tweetStreaming1 = TweetStreaming(self.rawTweetStreaming1)
        self.assertTrue(tweetStreaming0.equalHash(self.rawTweetStreaming0))
        self.assertTrue(tweetStreaming1.equalHash(self.rawTweetStreaming1))

    def test_tweetStreamingEqual(self):
        tweetStreaming0 = TweetStreaming(self.rawTweetStreaming0)
        tweetStreaming1 = TweetStreaming(self.rawTweetStreaming1)
        self.assertTrue(tweetStreaming0.equal(tweetStreaming0))
        self.assertFalse(tweetStreaming0.equal(tweetStreaming1))

    def test_tweetStreamingCreationInvalid(self):
        self.assertRaises(Exception, TweetStreaming, self.rawTweetStreaming2)
        self.assertRaises(Exception, TweetStreaming, self.rawTweetStreaming3)

    def test_tweetStreamingToHash(self):
        tweetStreaming0 = TweetStreaming(self.rawTweetStreaming0)
        tweetStreaming1 = TweetStreaming(self.rawTweetStreaming1)
        hashTweetStreaming0 = tweetStreaming0.toHash()
        hashTweetStreaming1 = tweetStreaming1.toHash()
        self.assertTrue(tweetStreaming0.equalHash(hashTweetStreaming0))
        self.assertTrue(tweetStreaming1.equalHash(hashTweetStreaming1))

    def test_TweetStreamingWithNone(self):
        self.rawTweetStreaming0["command"] = None
        tweetStreaming0 = TweetStreaming(self.rawTweetStreaming0)

###############################################################################
# test for TweetSearch object
#
###############################################################################
class TestTweetSearchObject(unittest.TestCase):
    def setUp(self):
        self.rawTweetSearch0 = randomTweetSearch(0, 0)
        self.rawTweetSearch1 = randomTweetSearch(1, 1)
        #Invalid TweetSearch, no tweet
        self.rawTweetSearch2 = randomTweetSearch(2, 2)
        del self.rawTweetSearch2["tweet"]
        #Invalid TweetSearch, no search
        self.rawTweetSearch3 = randomTweetSearch(3, 3)
        del self.rawTweetSearch3["search"]

    def test_tweetSearchCreationValid(self):
        tweetSearch0 = TweetSearch(self.rawTweetSearch0)
        tweetSearch1 = TweetSearch(self.rawTweetSearch1)
        self.assertTrue(tweetSearch0.equalHash(self.rawTweetSearch0))
        self.assertTrue(tweetSearch1.equalHash(self.rawTweetSearch1))

    def test_tweetSearchEqual(self):
        tweetSearch0 = TweetSearch(self.rawTweetSearch0)
        tweetSearch1 = TweetSearch(self.rawTweetSearch1)
        self.assertTrue(tweetSearch0.equal(tweetSearch0))
        self.assertFalse(tweetSearch0.equal(tweetSearch1))

    def test_tweetSearchCreationInvalid(self):
        self.assertRaises(Exception, TweetSearch, self.rawTweetSearch2)
        self.assertRaises(Exception, TweetSearch, self.rawTweetSearch3)

    def test_tweetSearchToHash(self):
        tweetSearch0 = TweetSearch(self.rawTweetSearch0)
        tweetSearch1 = TweetSearch(self.rawTweetSearch1)
        hashTweetSearch0 = tweetSearch0.toHash()
        hashTweetSearch1 = tweetSearch1.toHash()
        self.assertTrue(tweetSearch0.equalHash(hashTweetSearch0))
        self.assertTrue(tweetSearch1.equalHash(hashTweetSearch1))

    def test_tweetSearchWithNone(self):
        self.rawTweetSearch0["command"] = None
        tweetSearch0 = TweetSearch(self.rawTweetSearch0)

###############################################################################
# test for Streaming object
#
###############################################################################
class TestStreamingObject(unittest.TestCase):
    def setUp(self):
        self.rawStreaming0 = randomStreaming(0)
        self.rawStreaming1 = randomStreaming(1)
        #Invalid Streaming, no query
        self.rawStreaming2 = randomStreaming(2)
        del self.rawStreaming2["query"]
        #Invalid Streaming, no consumer
        self.rawStreaming3 = randomStreaming(3)
        del self.rawStreaming3["consumer"]

    def test_streamingCreationValid(self):
        streaming0 = Streaming(self.rawStreaming0)
        streaming1 = Streaming(self.rawStreaming1)
        self.assertTrue(streaming0.equalHash(self.rawStreaming0))
        self.assertTrue(streaming1.equalHash(self.rawStreaming1))

    def test_streamingEqual(self):
        streaming0 = Streaming(self.rawStreaming0)
        streaming1 = Streaming(self.rawStreaming1)
        self.assertTrue(streaming0.equal(streaming0))
        self.assertFalse(streaming0.equal(streaming1))

    def test_streamingCreationInvalid(self):
        self.assertRaises(Exception, Streaming, self.rawStreaming2)
        self.assertRaises(Exception, Streaming, self.rawStreaming3)

    def test_streamingToHash(self):
        streaming0 = Streaming(self.rawStreaming0)
        streaming1 = Streaming(self.rawStreaming1)
        hashStreaming0 = streaming0.toHash()
        hashStreaming1 = streaming1.toHash()
        self.assertTrue(streaming0.equalHash(hashStreaming0))
        self.assertTrue(streaming1.equalHash(hashStreaming1))

    def test_streamingWithNone(self):
        self.rawStreaming0["query"] = None
        streaming0 = Streaming(self.rawStreaming0)

###############################################################################
# test for Search object
#
###############################################################################
class TestSearchObject(unittest.TestCase):
    def setUp(self):
        self.rawSearch0 = randomSearch(0)
        self.rawSearch1 = randomSearch(1)
        #Invalid Search, no query
        self.rawSearch2 = randomSearch(2)
        del self.rawSearch2["query"]
        #Invalid Search, no consumer
        self.rawSearch3 = randomSearch(3)
        del self.rawSearch3["consumer"]

    def test_searchCreationValid(self):
        search0 = Search(self.rawSearch0)
        search1 = Search(self.rawSearch1)
        self.assertTrue(search0.equalHash(self.rawSearch0))
        self.assertTrue(search1.equalHash(self.rawSearch1))

    def test_searchEqual(self):
        search0 = Search(self.rawSearch0)
        search1 = Search(self.rawSearch1)
        self.assertTrue(search0.equal(search0))
        self.assertFalse(search0.equal(search1))

    def test_searchCreationInvalid(self):
        self.assertRaises(Exception, Search, self.rawSearch2)
        self.assertRaises(Exception, Search, self.rawSearch3)

    def test_searchToHash(self):
        search0 = Search(self.rawSearch0)
        search1 = Search(self.rawSearch1)
        hashSearch0 = search0.toHash()
        hashSearch1 = search1.toHash()
        self.assertTrue(search0.equalHash(hashSearch0))
        self.assertTrue(search1.equalHash(hashSearch1))

    def test_searchWithNone(self):
        self.rawSearch0["query"] = None
        search0 = Search(self.rawSearch0)

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
                outputStr += field["name"] + " = " + randomStringFixed(10) + "# Coment1"
            elif field["type"] == int:
                outputStr += "# Comment2 \n"
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

    def test_parseEncodeTweetStreaming(self):
        randomElements = randomInteger(100)
        for i in range(0, randomElements):
            tweetStreaming1 = TweetStreaming(randomTweetStreaming(i,i))
            encodeTweetStreaming1 = encodeObject(tweetStreaming1)
            tweetStreaming2 = parseText(encodeTweetStreaming1)
            self.assertTrue(tweetStreaming1.equal(tweetStreaming2))

    def test_parseEncodeTweetSearch(self):
        randomElements = randomInteger(100)
        for i in range(0, randomElements):
            tweetSearch1 = TweetSearch(randomTweetSearch(i,i))
            encodeTweetSearch1 = encodeObject(tweetSearch1)
            tweetSearch2 = parseText(encodeTweetSearch1)
            self.assertTrue(tweetSearch1.equal(tweetSearch2))

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

