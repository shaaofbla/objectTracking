import cv2
from utils.pivideostream import PiVideoStream
from utils.object import Object
import utils.TrackerConfig as config
from utils.Roi import Roi
from utils.Roi import fold
import time
import numpy as np


class Tracker:
    def __init__(self, lower=(0, 0, 0), upper=(255, 255, 255)):
        self.FilterLower = lower
        self.FilterUpper = upper
        self.Framerate = 33
        self.Frame = None
        self.CameraResolution = (640, 480)
        self.Resolution = (640, 480)
        self.MaxRadius = None
        self.setMaxRadius()
        self.videoStream = None
        self.Object = Object()
        self.Roi = Roi()

    def __del__(self):
        pass

    def config(self):
        self.FilterLower = config.FILTER_LOWER
        self.FilterUpper = config.FILTER_UPPER
        self.Framerate = config.FRAMERATE
        self.cameraResolution = config.CAMERA_RESOLUTION
        self.Resolution = config.RESOLUTION
        self.setMaxRadius()

    def setMaxRadius(self):
        maxRad = np.sqrt(np.sum(np.power(self.Resolution, 2)))
        self.MaxRadius = maxRad

    def start(self):
        print("stargin videostream")
        self.videoStream = PiVideoStream(framerate=self.Framerate,
                                         resolution=self.cameraResolution)
        self.videoStream.start()
        time.sleep(2)
        print("videostream started")
        return

    def close(self):
        self.videoStream.close()
        return

    def ProcessFrame(self):
        self.Frame = self.videoStream.read()
        print("Resolution:", self.Resolution)
        print("cameraResolution:", self.cameraResolution)
        print("original Frame:", self.Frame.shape)
        self.Frame = cv2.resize(self.Frame, self.Resolution)
        print("resized Frame:", self.Frame.shape)
        if self.Roi.x is None:
            RoiFrame = self.Frame
        else:
            RoiFrame = self.Frame[self.Roi.x:self.Roi.x2, self.Roi.y:self.Roi.y2]
        print("Roi shape:", RoiFrame.shape)
        print("Rois coords:", self.Roi.x, self.Roi.y, self.Roi.x2, self.Roi.y2)
            
        hsv = cv2.cvtColor(RoiFrame, cv2.COLOR_BGR2HSV)
        blure = cv2.GaussianBlur(hsv, (11, 11), 0)

        mask = cv2.inRange(blure, self.FilterLower, self.FilterUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        #self.mask = mask
        

        contours = cv2.findContours(mask.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contours) > 0:
            self.Object.Present = True
            largest_contour = max(contours, key=cv2.contourArea)
            self.getCoordinates(largest_contour)
            self.getMoments(largest_contour)
            self.getCenter()
            self.setRoi()

        else:
            self.Object.Present = False
            self.setRoiNone()

    def setRoi(self):
        f = 3.
        x = (self.Object.x - self.Object.radius*f)*self.Resolution[0]
        print("self.x", self.Object.x)
        print("self.r", self.Object.radius)
        print("self.Res", self.Resolution[0])
        x = int(fold(x,0,self.Resolution[0]))
        self.Roi.x = x
        print("set Roi x:", x)
        y = (self.Object.y - self.Object.radius*f)*self.Resolution[1]
        y = int(fold(y,0,self.Resolution[1]))
        self.Roi.y = y
        print("set Roi y:", y)
        w = int(self.Object.radius*2*f*self.Resolution[0])
        self.Roi.x2 = int(x+w)
        self.Roi.y2 = int(y+w)
        self.Roi.w = w

    def getCenter(self):
        M = self.Object.Moments
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        self.Object.Center = center

    def getMoments(self, contour):
        self.Object.Moments = cv2.moments(contour)
        return

    def getCoordinates(self, contour):
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        print("coords from cv3",x,y)
        if self.Roi.x is None:
            self.Object.x = x/self.Resolution[0]
            self.Object.y = y/self.Resolution[1]
        else:
            self.Object.x = x/self.Resolution[0] + 1./self.Roi.x
            self.Object.y = y/self.Resolution[1] + 1./self.Roi.y
        self.Object.radius = radius/self.MaxRadius
        return

    def RecordPath(self):
        self.Object.PathAppendPoint(self.Object.Center)

    def DrawCircle(self):
        cv2.circle(self.Frame,
                   (int(self.Object.x*self.Resolution[0]),
                    int(self.Object.y*self.Resolution[1])),
                   int(self.Object.radius),
                   (141, 255, 8), 2)
        cv2.circle(self.Frame,
                   (int(self.Object.x),
                    int(self.Object.y)),
                   5, (0, 141, 244), -1)

    def DrawSquare(self):
        cv2.rectangle(self.Frame, (self.Roi.x,self.Roi.y),(self.Roi.x2, self.Roi.y2), (255,0,255),1)

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
        for i in range(1, len(points)):
            if points[i-1] is None or points[i] is None:
                continue
            LineThickness = int(np.sqrt(64 / float(i+1)) * 1.5)
            cv2.line(self.Frame, points[i-1],
                     points[i], (8, 82, 255), LineThickness)
        return
