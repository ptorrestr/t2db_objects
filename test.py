#!/usr/bin/env python3

import random
import string
import unittest
import _thread as thread

from threading import Semaphore

from objects import User
from objects import Tweet
from objects import Job
from objects import Configuration
from objects import ObjectList
from objects import parseText
from objects import encodeObject
from objects import formatHash

from psocket import SocketServer
from psocket import SocketClient
from psocket import SocketControl

from utilities import readConfigFile
from utilities import writeFile
from utilities import removeFile

def randomInteger(maxSize):
    return random.randint(0, maxSize)

def randomBoolean():
    if randomInteger(2) == 0:
        return False
    return True

def randomStringFixed(size = 10, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def randomStringVariable(maxSize, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
    size = randomInteger(maxSize)
    return ''.join(random.choice(chars) for x in range(size))

def randomText(maxSizeText, maxSizeWord):
    text = ''
    size = randomInteger(maxSizeText)
    while len(text) < size:
        word = randomStringVariable(maxSizeWord)
        text += word + ' '
    return text[0:size]

def randomUrl(base, extension):
    text = "http://"
    text += base
    text += "/"
    text += randomStringVariable(20)
    text += "."
    text += extension
    return text

def randomTweet(id_, created_at, user):
    randomTweet = {}
    randomTweet['id'] = id_
    randomTweet['created_at'] = created_at
    randomTweet['user'] = user
    # Non-mandatory
    randomTweet['retweet_count'] = randomInteger(100)
    randomTweet['text'] = randomText(200, 20)
    randomTweet['in_reply_to_screen_name'] = randomStringVariable(50)
    randomTweet['in_reply_to_user_id'] = randomStringVariable(50)
    randomTweet['in_reply_to_status_id'] = randomStringVariable(50)
    randomTweet['source'] = randomStringVariable(50)
    randomTweet['urls'] = randomUrl("twitter.com", "html")
    randomTweet['user_mentions'] = randomStringVariable(50)
    randomTweet['hashtags'] = randomText(100,10)
    randomTweet['geo'] = randomStringVariable(50)
    randomTweet['place'] = randomStringVariable(50)
    randomTweet['coordinates'] = randomStringFixed(10)
    randomTweet['contributors'] = randomStringVariable(50)
    randomTweet['favorited'] = randomBoolean()
    randomTweet['truncated'] = randomBoolean()
    randomTweet['retweeted'] = randomBoolean()
    return randomTweet

def randomUser(id_, created_at, name):
    randomUser = {}
    randomUser['id'] = id_
    randomUser['created_at'] = created_at
    randomUser['name'] = name
    # Non-mandatory
    randomUser['screen_name'] = randomStringVariable(200)
    randomUser['location'] = randomStringVariable(200)
    randomUser['description'] = randomText(200, 15)
    randomUser['profile_image_url'] = randomUrl("twitter.com", "jpg")
    randomUser['profile_image_url_https'] = randomUrl("twitter.com", "jpg")
    randomUser['profile_background_tile'] = randomBoolean()
    randomUser['profile_background_image_url'] = randomUrl("twitter.com", "jpg")
    randomUser['profile_background_color'] = randomStringFixed(6)
    randomUser['profile_sidebar_fill_color'] = randomStringFixed(6)
    randomUser['profile_sidebar_border_color'] = randomStringFixed(6)
    randomUser['profile_link_color'] = randomStringFixed(6)
    randomUser['profile_text_color'] = randomStringFixed(6)
    randomUser['protected'] = randomBoolean()
    randomUser['utc_offset'] = randomInteger(100)
    randomUser['time_zone'] = randomStringFixed(3)
    randomUser['followers_count'] = randomInteger(100)
    randomUser['friends_count'] = randomInteger(100)
    randomUser['statuses_count'] = randomInteger(100)
    randomUser['favourites_count'] = randomInteger(100)
    randomUser['url'] = randomUrl("usersite.com", ".html")
    randomUser['geo_enabled'] = randomBoolean()
    randomUser['verified'] = randomBoolean()
    randomUser['lang'] = randomStringFixed(2)
    randomUser['notifications'] = randomBoolean()
    randomUser['contributors_enabled'] = randomBoolean()
    randomUser['listed_count'] = randomInteger(100)
    return randomUser

def randomJob(command, process_id):
    randomJob = {}
    randomJob['command'] = command
    randomJob['process_id'] = process_id
    # Non-mandatory
    randomJob['consumer'] = randomStringFixed(100)
    randomJob['consumer_sec'] = randomStringFixed(100)
    randomJob['access'] = randomStringFixed(100)
    randomJob['access_sec'] = randomStringFixed(100)
    randomJob['query'] = randomText(100, 10)
    randomJob['kind'] = randomStringFixed(5)
    return randomJob

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

###############################################################################
# Test for SOCKET objects
#
###############################################################################
sharedList = []
sharedListLock = Semaphore(0)

def sendObject(host, port, objectToSend):
    sock = SocketClient(host, port).getSocketControl()
    sock.sendObject(objectToSend)
    sock.close()

def receiveObject(host,  port):
    sock = SocketClient(host, port).getSocketControl()
    objectReceived = sock.recvObject()
    sharedList.append(objectReceived)
    sharedListLock.release()
    sock.close()

def sendData(host, port, data):
    sock = SocketClient(host, port).getSocketControl()
    sock.send(data)
    sock.close()

def receiveData(host, port):
    sock = SocketClient(host, port).getSocketControl()
    data = sock.recv()
    sharedList.append(data)
    sharedListLock.release()
    sock.close()
    

class TestSocketObject(unittest.TestCase):
    def setUp(self):
        # Re-start global variables
        global sharedList
        global sharedListLock
        sharedList = []
        sharedListLock = Semaphore(0)
        # Start new server
        self.server = SocketServer(port = 1300, maxConnection = 5)

    # Test TWEET, send and receive
    def test_sendTweet(self):
        tweet1 = Tweet(randomTweet(0, "date", 0))
        thread.start_new_thread(receiveObject, (self.server.getHostName(), 1300,))
        socketControl = self.server.accept()
        socketControl.sendObject(tweet1)
        sharedListLock.acquire()
        tweet2 = sharedList[0]
        self.assertTrue(tweet1.equal(tweet2))
        socketControl.close()
    
    def test_receiveTweet(self):
        tweet1 = Tweet(randomTweet(0, "date", 0))
        thread.start_new_thread(sendObject, (self.server.getHostName(), 1300, tweet1,))
        socketControl = self.server.accept()
        tweet2 = socketControl.recvObject()
        self.assertTrue(tweet1.equal(tweet2))
        socketControl.close()

    # Test USER, send and receive
    def test_sendUser(self):
        user1 = User(randomUser(0, "date", "user0"))
        thread.start_new_thread(receiveObject, (self.server.getHostName(), 1300,))
        socketControl = self.server.accept()
        socketControl.sendObject(user1)
        sharedListLock.acquire()
        user2 = sharedList[0]
        self.assertTrue(user1.equal(user2))
        socketControl.close()

    def test_receiveUser(self):
        user1 = User(randomUser(0, "date", "user0"))
        thread.start_new_thread(sendObject, (self.server.getHostName(), 1300, user1,))
        socketControl = self.server.accept()
        user2 = socketControl.recvObject()
        self.assertTrue(user1.equal(user2))
        socketControl.close()

    # Test JOB, send and receive
    def test_sendJob(self):
        job1 = Job(randomJob("START", 0))
        thread.start_new_thread(receiveObject, (self.server.getHostName(), 1300,))
        socketControl = self.server.accept()
        socketControl.sendObject(job1)
        sharedListLock.acquire()
        job2 = sharedList[0]
        self.assertTrue(job1.equal(job2))
        socketControl.close()

    def test_receiveJob(self):
        job1 = Job(randomJob("START", 0))
        thread.start_new_thread(sendObject, (self.server.getHostName(), 1300, job1,))
        socketControl = self.server.accept()
        job2 = socketControl.recvObject()
        self.assertTrue(job1.equal(job2))
        socketControl.close()

    # Test OBJECTLIST, send and receive
    def test_sendObjectList(self):
        randomElements = randomInteger(100)
        objectList1 = ObjectList()
        for i in range(0, randomElements):
            element = User(randomUser(i, "date", "user0"))
            objectList1.append(element)

        thread.start_new_thread(receiveObject, (self.server.getHostName(), 1300,))
        socketControl = self.server.accept()
        socketControl.sendObject(objectList1)
        sharedListLock.acquire()
        objectList2 = sharedList[0]

        internalList1 = objectList1.getList()
        internalList2 = objectList2.getList()
        for i in range(0, randomElements):
            self.assertTrue(internalList1[i].equal(internalList2[i]) )
        socketControl.close()

    def test_receiveObjectList(self):
        randomElements = randomInteger(100)
        objectList1 = ObjectList()
        for i in range(0, randomElements):
            element = User(randomUser(i, "date", "user0"))
            objectList1.append(element)

        thread.start_new_thread(sendObject, (self.server.getHostName(), 1300, objectList1,))
        socketControl = self.server.accept()
        objectList2 = socketControl.recvObject()

        internalList1 = objectList1.getList()
        internalList2 = objectList2.getList()
        for i in range(0, randomElements):
            self.assertTrue(internalList1[i].equal(internalList2[i]) )
        socketControl.close()

    # Test data size 19Kb (max 32 Tb)
    def test_sendData(self):
        for i in range(1, 200):
            data1 = randomStringFixed(i*100)
            thread.start_new_thread(receiveData, (self.server.getHostName(), 1300,))
            socketControl = self.server.accept()
            socketControl.send(data1)
            sharedListLock.acquire()
            data2 = sharedList[i-1]
            self.assertTrue(len(data1) == len(data2))
            self.assertTrue(data1 == data2 )
            socketControl.close()

    def test_recvData(self):
        for i in range(1, 200):
            data1 = randomStringFixed(i*100)
            thread.start_new_thread(sendData, (self.server.getHostName(), 1300, data1,))
            socketControl = self.server.accept()
            data2 = socketControl.recv()
            self.assertTrue(len(data1) == len(data2))
            self.assertTrue(data1 == data2 )
            socketControl.close()

    def tearDown(self):
        #Close server
        self.server.close()

if __name__ == '__main__':
    unittest.main()
