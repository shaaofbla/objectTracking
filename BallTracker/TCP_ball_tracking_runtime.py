from tracker.tracker import Tracker
from imutils.video import FPS
from TCP.client import client
import socket

TCPclient = client()
TCPclient.config()
TCPclient.connect()


BallTracker = Tracker()
BallTracker.config()
BallTracker.start()

fps = FPS().start()

while True:
    try:
        BallTracker.ProcessFrame()
        if BallTracker.Object.Present:
            if BallTracker.Object.radius > 10:
                TCPclient.sendxyr(BallTracker)
        fps.update()

    except KeyboardInterrupt:
        break
    except socket.error as e:
        print e
        print "restarting client"
        TCPclient.close()
        del TCPclient
        TCPclient = client()
        TCPclient.config()
        TCPclient.connect()
        continue

fps.stop()

print "FPS: {:.2f}".format(fps.fps())
TCPclient.close()
BallTracker.close()
del BallTracker
