#!/usr/bin/env python3
# psocket.py tests

import unittest
import _thread as thread
from threading import Semaphore

from t2db_objects.objects import User
from t2db_objects.objects import Tweet
from t2db_objects.objects import Job
from t2db_objects.objects import Configuration
from t2db_objects.objects import ObjectList
from t2db_objects.objects import parseText
from t2db_objects.objects import encodeObject
from t2db_objects.objects import formatHash

from t2db_objects.psocket import SocketServer
from t2db_objects.psocket import SocketClient
from t2db_objects.psocket import SocketControl

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
