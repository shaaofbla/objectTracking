from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from collections import deque
import numpy as np
import time
import cv2
import socket

#TCP settings
TCP_IP = '192.168.0.11'
TCP_PORT = 5005
BUFFER_SIZE = 60
SEND2TCP = True

#Output settings
SHOW = False
SHOW_CIRCLE = False
SHOW_PATH = False
if SEND2TCP:
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sok.connect((TCP_IP, TCP_PORT))

#initialize picamera
#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 25
#rawCapture = PiRGBArray(camera, size=(640, 480))

videoStream = PiVideoStream(framerate=10).start()

time.sleep(2.0)
fps = FPS().start()

#define color range
greenLower = (57, 165, 39)
greenUpper = (100, 255, 255)

pts = deque(maxlen=64)

while True:
    frame = videoStream.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.GaussianBlur(hsv, (11,11),0)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        p = "normal"
        c = max(cnts, key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if cv2.contourArea(c)< 500:
            continue

        if radius > 10:
            if SHOW_CIRCLE:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255,255), 2)
                cv2.circle(frame, center, 5, (0,0,255), -1)
            if SEND2TCP:
                message = "{0}\t{1}\t{2}".format(round(x,2),round(y,2),round(radius,2))
                sok.send(message)

    pts.appendleft(center)
    if SHOW & SHOW_PATH:
        for i in xrange(1, len(pts)):
            if pts[i-1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(64 / float(i+1)) * 2.5)
            cv2.line(frame, pts[i-1], pts[i], (0,0,255), thickness)

    if SHOW:
        cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    fps.update()

    if key == ord("q"):
        break
fps.stop()
print "FPS: {:.2f}".format(fps.fps())
if SEND2TCP:
    sok.close()
if SHOW:
    cv2.destroyAllWindows()
videoStream.stop()
