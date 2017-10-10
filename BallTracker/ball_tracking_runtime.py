from utils.pivideostream import PiVideoStream
from tracker.tracker import Tracker
from imutils.video import FPS
from TCP.client import client
import numpy as np
import time
import cv2

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
                message = "{:.2f}\t{:.2f}\t{:.2f}".format(BallTracker.Object.x,BallTracker.Object.y,BallTracker.Object.radius)
                TCPclient.send(message)

        fps.update()

    except KeyboardInterrupt:
        break

fps.stop()

print "FPS: {:.2f}".format(fps.fps())
TCPclient.close()
BallTracker.close()
del BallTracker
