from picamera.array import PiRGBArray
from picamera import PiCamera
from collections import deque
import numpy as np
import time
import cv2

#initialize picamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

#define color range
greenLower = (20, 105, 36)
greenUpper = (155, 255, 255)

pts = deque(maxlen=64)

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
    frame = frame.array
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
            rawCapture.truncate(0)
            continue
            p = "continue"

        print p
        
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255,255), 2)
            cv2.circle(frame, center, 5, (0,0,255), -1)
    pts.appendleft(center)
    for i in xrange(1, len(pts)):
        if pts[i-1] is None or pts[i] is None:
            continue
        thickness = int(np.sqrt(64 / float(i+1)) * 2.5)
        cv2.line(frame, pts[i-1], pts[i], (0,0,255), thickness)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break

cv2.destroyAllWindows()
