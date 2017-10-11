import socket
import time
import utils.TrackerConfig as config

class client:
    def __init__(self,ip='192.168.0.11',port=5005,buffer_size=60):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def config(self):
        self.ip = config.TCP_IP
        self.port = config.TCP_PORT
        self.buffer_size = config.BUFFER_SIZE

    def connect(self):
        while True:
            try:
                self.socket.connect((self.ip, self.port))
                print "connected to: ", self.ip
                return
            except Exception as exc:
                print "Caught exception socket.error: %s" % exc
                print "Couln't connect, try again in a moment."
                time.sleep(5)
            except KeyboardInterrupt:
                return

    def send(self,message):
        self.socket.send(message)
        return

    def sendxyr(self, tracker):
        x = tracker.Object.x
        y = tracker.Object.y
        r = tracker.Object.radius
        message = "{:.2f}\t{:.2f}\t{:.2f}\t".format(x,y,r)
        self.send(message)

    def close(self):
        self.socket.close()
        return
