import cv2
from utils.pivideostream import PiVideoStream
from utils.object import Object
import utils.TrackerConfig as config
import time
import numpy as np


class Tracker:
    def __init__(self, lower=(0, 0, 0), upper=(255, 255, 255)):
        self.FilterLower = lower
        self.FilterUpper = upper
        self.Framerate = 33
        self.Frame = None
        self.Resolution = (640, 480)
        self.MaxRadius = None
        self.setMaxRadius()
        self.videoStream = None
        self.Object = Object()

    def __del__(self):
        pass

    def config(self):
        self.FilterLower = config.FILTER_LOWER
        self.FilterUpper = config.FILTER_UPPER
        self.Framerate = config.FRAMERATE
        self.Resolution = config.RESOLUTION
        self.setMaxRadius()

    def setMaxRadius(self):
        maxRad = np.sqrt(np.sum(np.power(self.Resolution, 2)))
        self.MaxRadius = maxRad
        print(self.MaxRadius)

    def start(self):
        self.videoStream = PiVideoStream(framerate=self.Framerate,
                                         resolution=self.Resolution)
        self.videoStream.start()
        time.sleep(2)
        return

    def close(self):
        self.videoStream.close()
        return

    def ProcessFrame(self):
        frame = self.videoStream.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blure = cv2.GaussianBlur(hsv, (11, 11), 0)

        mask = cv2.inRange(blure, self.FilterLower, self.FilterUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        self.mask = mask

        contours = cv2.findContours(mask.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contours) > 0:
            self.Object.Present = True
            largest_contour = max(contours, key=cv2.contourArea)
            self.getCoordinates(largest_contour)
            self.getMoments(largest_contour)
            self.getCenter()
        else:
            self.Object.Present = False

    def getCenter(self):
        M = self.Object.Moments
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        self.Object.Center = center

    def getMoments(self, contour):
        self.Object.Moments = cv2.moments(contour)
        return

    def getCoordinates(self, contour):
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        self.Object.x = x/self.Resolution[0]
        self.Object.y = y/self.Resolution[1]
        self.Object.radius = radius/self.MaxRadius
        return

    def RecordPath(self):
        self.Object.PathAppendPoint(self.Object.Center)

    def DrawCircle(self):
        cv2.circle(self.Frame,
                   (int(self.Object.x),
                    int(self.Object.y)),
                   int(self.Object.radius),
                   (141, 255, 8), 2)
        cv2.circle(self.Frame,
                   (int(self.Object.x),
                    int(self.Object.y)),
                   5, (0, 141, 244), -1)

    def DrawCoordinates(self):
        cv2.putText(self.Frame,
                    "x: {:.2f} -  y: {:.2f}".format(self.Object.x,
                                                    self.Object.y),
                    (10, int(self.Resolution[1])-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (255, 255, 50), 1, cv2.LINE_AA)

    def DrawScreenCenter(self):
        color = (255, 15, 65)
        thik = 1
        cv2.line(self.Frame, (0, 0), (self.Resolution), color, thik)
        cv2.line(self.Frame, (self.Resolution[0], 0),
                 (0, self.Resolution[1]), color, thik)

    def DrawPath(self):
        points = self.Object.Path
        for i in xrange(1, len(points)):
            if points[i-1] is None or points[i] is None:
                continue
            LineThickness = int(np.sqrt(64 / float(i+1)) * 1.5)
            cv2.line(self.Frame, points[i-1],
                     points[i], (8, 82, 255), LineThickness)
        return
