#socket connection for python3
import socket
import time

from .objects import parseText
from .objects import encodeObject

## Class to control socket communication
class SocketControl(object):
    def __init__(self, sock):
        self.sock = sock

    def sendObject(self, objectToSend):
        msg = encodeObject(objectToSend)
        self.send(msg)

    def send(self, msg, strEncoding = "utf-8", chunk = 4096):
        msgBytes = bytes(msg, strEncoding)
        msgBytesLength = len(msgBytes)
        # Determine how many chunk does msg need
        numberChunks = int(msgBytesLength / chunk)
        if msgBytesLength % chunk > 0:
            numberChunks += 1
        # Send number of chunks
        strNumberChunks = str(numberChunks)
        sent1 = self.sock.send(bytes(strNumberChunks, strEncoding))
        # Wait confirmation
        recv1 = self.sock.recv(2)
        # Send the message in chunks
        begin = 0
        for i in range(0, numberChunks):
            end = begin + chunk
            sent2 = self.sock.send(msgBytes[begin:end])
            begin += chunk
        # Force synchronisation
        recv2 = self.sock.recv(2)

    def recvObject(self):
        msg = self.recv()
        return parseText(msg)

    def recv(self, strEncoding = "utf-8", chunk = 4096):
        # receive number of chunks
        strNumberChunks = self.sock.recv(10)
        numberChunks = int(strNumberChunks)
        # send confirmation
        confirmation = "ok"
        sent1 = self.sock.send(bytes(confirmation, strEncoding))
        # receive the message
        msgBytes = bytearray()
        for i in range(0, numberChunks):
            msgBytes += self.sock.recv(chunk)
        # Force synchronisation
        sent2 = self.sock.send(bytes(confirmation, strEncoding))
        return msgBytes.decode(strEncoding)
        

    def close(self):
        self.sock.close()

class SocketServer(object):
    def __init__(self, port, maxConnection):
        if type(port) is not int:
            raise Exception("Port is invalid")
        if type(maxConnection) is not int:
            raise Exception("MaxConnection is invalid")
        self.sockserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockserver.bind((socket.gethostname(), port))
        self.sockserver.listen(maxConnection)

    def setTimeout(self, timeout):
        self.sockserver.settimeout(timeout)
        
    # Wait for incoming connections. Return the SocketControl for communcation.
    def accept(self):
        [sock, address] = self.sockserver.accept()
        return SocketControl(sock)

    def getHostName(self):
        return socket.gethostname()

    def close(self):
        self.sockserver.close()
        
class SocketClient(object):
    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(address), port))

    def getSocketControl(self):
        return SocketControl(self.sock)

    def close(self):
        self.sock.close()
    

