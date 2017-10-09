from utils.pivideostream import PiVideoStream
from tracker.tracker import Tracker
from imutils.video import FPS
from TCP.client import client
import numpy as np
import time
import cv2

#TCP settings
TCP_IP = '192.168.0.11'
TCP_PORT = 5005
BUFFER_SIZE = 60
SEND2TCP = False
TCPclient = client(TCP_IP,TCP_PORT,BUFFER_SIZE)

#Output settings
SHOW = True
SHOW_CIRCLE = True
SHOW_PATH = False

#define color range
greenLower = (57, 165, 39)
greenUpper = (100, 255, 255)

BallTracker = Tracker(greenLower, greenUpper)
BallTracker.start()

fps = FPS().start()

while True:
    BallTracker.ProcessFrame()
    if BallTracker.Object.Present:
        if BallTracker.Object.radius > 10:
            if SHOW_CIRCLE:
                BallTracker.DrawCircle()
            if SEND2TCP:
                message = "{0}\t{1}\t{2}".format(round(x,2),round(y,2),round(radius,2))
                TCPclient.send(message)

        BallTracker.RecordPath()

    if SHOW & SHOW_PATH:
        for i in xrange(1, len(BallTracker.Object.Path)):
            pts = BallTracker.Object.Path
            if pts[i-1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(64 / float(i+1)) * 2.5)
            cv2.line(frame, pts[i-1], pts[i], (0,0,255), thickness)

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
