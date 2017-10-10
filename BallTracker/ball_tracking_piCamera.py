from utils.pivideostream import PiVideoStream
from tracker.tracker import Tracker
from imutils.video import FPS
from TCP.client import client
from utils.TrackerConfig import TCP_IP, TCP_PORT, BUFFER_SIZE, SEND2TCP
from utils.TrackerConfig import SHOW, SHOW_CIRCLE, SHOW_PATH
import numpy as np
import time
import cv2

TCPclient = client(TCP_IP,TCP_PORT,BUFFER_SIZE)
TCPclient.connect()


BallTracker = Tracker()
BallTracker.config()
BallTracker.start()

fps = FPS().start()

while True:
    BallTracker.ProcessFrame()
    if BallTracker.Object.Present:
        if BallTracker.Object.radius > 10:
            if SHOW_CIRCLE:
                BallTracker.DrawCircle()
            if SEND2TCP:
                message = "{:.2f}\t{:.2f}\t{:.2f}".format(BallTracker.Object.x,BallTracker.Object.y,BallTracker.Object.radius)
                TCPclient.send(message)

        BallTracker.RecordPath()

    if SHOW_PATH:
        BallTracker.DrawPath()

    if SHOW:
        cv2.imshow("Frame", BallTracker.videoStream.frame)
    key = cv2.waitKey(1) & 0xFF

    fps.update()

    if key == ord("q"):
        break
    pts = BallTracker.Object.Path

fps.stop()
print "FPS: {:.2f}".format(fps.fps())
if SEND2TCP:
    client.close()
if SHOW:
    cv2.destroyAllWindows()

BallTracker.close()
del BallTracker
