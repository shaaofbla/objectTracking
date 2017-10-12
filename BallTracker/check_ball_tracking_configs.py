from utils.pivideostream import PiVideoStream
from tracker.tracker import Tracker
from imutils.video import FPS
from TCP.client import client
from utils.TrackerConfig import SEND2TCP
from utils.TrackerConfig import SHOW, SHOW_CIRCLE, SHOW_PATH, SHOW_COORDINATES, SHOW_SCREEN_CENTER
import numpy as np
import time
import socket
import cv2
#import sys #get rid of this

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
        BallTracker.RecordPath()
        if BallTracker.Object.Present:
            if BallTracker.Object.radius > 10:
                if SHOW_PATH:
                    BallTracker.DrawPath()

                if SHOW_CIRCLE:
                    BallTracker.DrawCircle()

                if SEND2TCP:
                    TCPclient.sendxyr(BallTracker)
            #BallTracker.RecordPath()
                if SHOW_COORDINATES:
                    BallTracker.DrawCoordinates()

                if SHOW_SCREEN_CENTER:
                    BallTracker.DrawScreenCenter()

                if SHOW:
                    cv2.imshow("Frame", BallTracker.videoStream.frame)

        key = cv2.waitKey(1) & 0xFF
        fps.update()

        if key == ord("q"):
            print key
            raise

    except KeyboardInterrupt:
        break

    except socket.error as e:
        print e
        print "[Main] Restarting client"
        TCPclient.close()
        del TCPclient
        TCPclient = client()
        TCPclient.config()
        TCPclient.connect()
        continue

fps.stop()
print "FPS: {:.2f}".format(fps.fps())
if SEND2TCP:
    TCPclient.close()
if SHOW:
    cv2.destroyAllWindows()

BallTracker.close()
del BallTracker
