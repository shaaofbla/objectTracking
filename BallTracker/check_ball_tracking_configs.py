from utils.pivideostream import PiVideoStream
from tracker.tracker import Tracker
from imutils.video import FPS
from TCP.client import client
from utils.TrackerConfig import SEND2TCP
from utils.TrackerConfig import SHOW, SHOW_CIRCLE, SHOW_PATH
import numpy as np
import time
import cv2
import sys #get rid of this

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
                if SHOW_CIRCLE:
                    BallTracker.DrawCircle()
                if SEND2TCP:
                    TCPclient.sendxyr(BallTracker)

            BallTracker.RecordPath()

        if SHOW_PATH:
            BallTracker.DrawPath()

        if SHOW:
            cv2.imshow("Frame", BallTracker.videoStream.frame)

        key = cv2.waitKey(1) & 0xFF
        fps.update()

        if key == ord("q"):
            print key
            raise

    except KeyboardInterrupt:
        break

    except:
        e = sys.exc_info()[0]
        print e
        break

fps.stop()
print "FPS: {:.2f}".format(fps.fps())
if SEND2TCP:
    TCPclient.close()
if SHOW:
    cv2.destroyAllWindows()

BallTracker.close()
del BallTracker
