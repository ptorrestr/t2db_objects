import unittest
import time
import _thread as thread
from threading import Semaphore

from t2db_objects.objects import User
from t2db_objects.objects import Tweet
from t2db_objects.objects import TweetStreaming
from t2db_objects.objects import TweetSearch
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
from t2db_objects.tests.common import randomTweetStreaming
from t2db_objects.tests.common import randomTweetSearch
from t2db_objects.tests.common import randomJob


###############################################################################
# Test for SOCKET objects
#
###############################################################################
sharedList = []
sharedListLock = Semaphore(0)
port1 = 13000
port2 = 13001
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

def receiveObjectMany(host, port):
    sock = SocketClient(host, port).getSocketControl()
    data1 = sock.recvObject()
    data2 = sock.recvObject()
    data3 = sock.recvObject()
    data4 = sock.recvObject()
    sharedList.append(data1)
    sharedList.append(data2)
    sharedList.append(data3)
    sharedList.append(data4)
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

def receiveDataMany(host, port):
    sock = SocketClient(host, port).getSocketControl()
    data1 = sock.recv()
    data2 = sock.recv()
    data3 = sock.recv()
    data4 = sock.recv()
    sharedList.append(data1)
    sharedList.append(data2)
    sharedList.append(data3)
    sharedList.append(data4)
    sharedListLock.release()
    sock.close()    

@unittest.skip("Avoiding psockets")
class TestSocketObject(unittest.TestCase):
    def setUp(self):
        # Re-start global variables
        global sharedList
        global sharedListLock
        sharedList = []
        sharedListLock = Semaphore(0)
        # Start new server
        self.server = SocketServer(port = port1, maxConnection = 5)

    # Test TWEET, send and receive
    def test_sendTweet(self):
        tweet1 = Tweet(randomTweet(0, "date", 0))
        thread.start_new_thread(receiveObject, (self.server.getHostName(), port1,))
        socketControl = self.server.accept()
        socketControl.sendObject(tweet1)
        sharedListLock.acquire()
        tweet2 = sharedList[0]
        self.assertTrue(tweet1.equal(tweet2))
        socketControl.close()
    
    def test_receiveTweet(self):
        tweet1 = Tweet(randomTweet(0, "date", 0))
        thread.start_new_thread(sendObject, (self.server.getHostName(), port1, tweet1,))
        socketControl = self.server.accept()
        tweet2 = socketControl.recvObject()
        self.assertTrue(tweet1.equal(tweet2))
        socketControl.close()

    # Test USER, send and receive
    def test_sendUser(self):
        user1 = User(randomUser(0, "date", "user0"))
        thread.start_new_thread(receiveObject, (self.server.getHostName(), port1,))
        socketControl = self.server.accept()
        socketControl.sendObject(user1)
        sharedListLock.acquire()
        user2 = sharedList[0]
        self.assertTrue(user1.equal(user2))
        socketControl.close()

    def test_receiveUser(self):
        user1 = User(randomUser(0, "date", "user0"))
        thread.start_new_thread(sendObject, (self.server.getHostName(), port1, user1,))
        socketControl = self.server.accept()
        user2 = socketControl.recvObject()
        self.assertTrue(user1.equal(user2))
        socketControl.close()

    # Test JOB, send and receive
    def test_sendJob(self):
        job1 = Job(randomJob("START", 0))
        thread.start_new_thread(receiveObject, (self.server.getHostName(), port1,))
        socketControl = self.server.accept()
        socketControl.sendObject(job1)
        sharedListLock.acquire()
        job2 = sharedList[0]
        self.assertTrue(job1.equal(job2))
        socketControl.close()

    def test_receiveJob(self):
        job1 = Job(randomJob("START", 0))
        thread.start_new_thread(sendObject, (self.server.getHostName(), port1, job1,))
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
        thread.start_new_thread(receiveObject, (self.server.getHostName(), port1,))
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
        thread.start_new_thread(sendObject, (self.server.getHostName(), port1, objectList1,))
        socketControl = self.server.accept()
        objectList2 = socketControl.recvObject()
        internalList1 = objectList1.getList()
        internalList2 = objectList2.getList()
        for i in range(0, randomElements):
            self.assertTrue(internalList1[i].equal(internalList2[i]) )
        socketControl.close()

    # Send data with different charsets
    def test_sendObjectListCharset(self):
        randomElements = 1000#randomInteger(100)
        objectList1 = ObjectList()
        for i in range(0, randomElements):
            element = User(randomUser(i, "áßðáßð213l21h", "œƒð©þ¥ú¥"))
            objectList1.append(element)        
        thread.start_new_thread(receiveObject, (self.server.getHostName(), port1,))
        socketControl = self.server.accept()
        socketControl.sendObject(objectList1)
        sharedListLock.acquire()
        objectList2 = sharedList[0]
        internalList1 = objectList1.getList()
        internalList2 = objectList2.getList()
        for i in range(0, randomElements):
            self.assertTrue(internalList1[i].equal(internalList2[i]) )
        socketControl.close()

    def test_sendObjectListMany(self):
        randomElements = 100
        objectList1 = ObjectList()
        for i in range(0, randomElements):
            element = Tweet(randomTweet(i, "date", i))
            objectList1.append(element)
        objectList2 = ObjectList()
        for i in range(0, randomElements):
            element = User(randomUser(i, "áßðáßð213l21h", "œƒð©þ¥ú¥"))
            objectList2.append(element)
        objectList3 = ObjectList()
        for i in range(0, randomElements):
            element = TweetStreaming(randomTweetStreaming(i, i))
            objectList3.append(element)
        objectList4 = ObjectList()
        for i in range(0, randomElements):
            element = TweetSearch(randomTweetSearch(i, i))
            objectList4.append(element)
        thread.start_new_thread(receiveObjectMany,
            (self.server.getHostName(), port1,))
        socketControl = self.server.accept()
        socketControl.sendObject(objectList1)
        socketControl.sendObject(objectList2)
        socketControl.sendObject(objectList3)
        socketControl.sendObject(objectList4)
        sharedListLock.acquire()
        objectList21 = sharedList[0]
        objectList22 = sharedList[1]
        objectList23 = sharedList[2]
        objectList24 = sharedList[3]
        internalList11 = objectList1.getList()
        internalList12 = objectList2.getList()
        internalList13 = objectList3.getList()
        internalList14 = objectList4.getList()
        internalList21 = objectList21.getList()
        internalList22 = objectList22.getList()
        internalList23 = objectList23.getList()
        internalList24 = objectList24.getList()
        self.assertTrue(internalList11[i].equal(internalList21[i]) )
        self.assertTrue(internalList12[i].equal(internalList22[i]) )
        self.assertTrue(internalList13[i].equal(internalList23[i]) )
        self.assertTrue(internalList14[i].equal(internalList24[i]) )
        socketControl.close()

    # Test data size 19Kb (max 32 Tb)
    def test_sendData(self):
        for i in range(1, 200):
            data1 = randomStringFixed(i*100)
            thread.start_new_thread(receiveData, (self.server.getHostName(), port1,))
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
            thread.start_new_thread(sendData, (self.server.getHostName(), port1, data1,))
            socketControl = self.server.accept()
            data2 = socketControl.recv()
            self.assertTrue(len(data1) == len(data2))
            self.assertTrue(data1 == data2 )
            socketControl.close()
    
    def test_sendDataMany(self):
        data1 = randomStringFixed(100)
        data2 = randomStringFixed(100)
        data3 = randomStringFixed(100)
        data4 = randomStringFixed(100)
        thread.start_new_thread(receiveDataMany, (self.server.getHostName(), port1,))
        socketControl = self.server.accept()
        socketControl.send(data1)
        socketControl.send(data2)
        socketControl.send(data3)
        socketControl.send(data4)
        sharedListLock.acquire()
        data21 = sharedList[0]
        data22 = sharedList[1]
        data23 = sharedList[2]
        data24 = sharedList[3]
        self.assertEqual(len(data1), len(data21))
        self.assertEqual(len(data2), len(data22))
        self.assertEqual(len(data3), len(data23))
        self.assertEqual(len(data4), len(data24))
        socketControl.close()

    def tearDown(self):
        #Close server
        self.server.close()


class TestSocketTimeout(unittest.TestCase):
    def setUp(self):
        # Re-start global variables
        global sharedList
        global sharedListLock
        sharedList = []
        sharedListLock = Semaphore(0)
        # Start new server
        self.server = SocketServer(port = port2, maxConnection = 5)
        self.server.setTimeout(5)

    def test_nonBlockingAccept(self):
        timeStart = time.time()
        # wait for connections
        # No connection received, stop in 5 sec, generate exception.
        self.assertRaises(Exception, self.server.accept)

    def test_blockingRecv(self):
        data1 = randomStringFixed(100)
        thread.start_new_thread(sendData, (self.server.getHostName(), port2, data1,))
        socketControl = self.server.accept()
        self.server.setTimeout(None)
        #time.sleep(5)
        data2 = socketControl.recv()
        self.assertTrue(len(data1) == len(data2))
        self.assertTrue(data1 == data2 )
        socketControl.close()

    def test_blockingSend(self):
        data1 = randomStringFixed(100)
        thread.start_new_thread(receiveData, (self.server.getHostName(), port2,))
        socketControl = self.server.accept()
        self.server.setTimeout(None)
        #time.sleep(5)
        socketControl.send(data1)
        sharedListLock.acquire()
        data2 = sharedList[0]
        self.assertTrue(len(data1) == len(data2))
        self.assertTrue(data1 == data2 )
        socketControl.close()

    def tearDown(self):
        #Close server
        self.server.close()
