import socket
import time

class client:
    def __init__(self,ip='192.168.0.11',port=5005,buffer_size=60):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.ip, self.port))
            return
        except Exception as exc:
            print "Caught exception socket.error: %s" % exc

    def send(self,message):
        self.socket.send(message)
        return

    def close(self):
        self.socket.close()
        return
