#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import colorsys
import os
import time


def callback(value):
    pass


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)


def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)

    return values


def main(configFile):
    range_filter = 'HSV'
    camera = cv2.VideoCapture(0)

    setup_trackbars(range_filter)

    # init picamera
    camera = PiCamera()
    camera.resolution = (320, 240)
    rawCapture = PiRGBArray(camera, size=(320, 240))
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame.array
        frame_to_thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        H_min, S_min, V_min, H_max, S_max, V_max = get_trackbar_values(range_filter)

        thresh = cv2.inRange(frame_to_thresh,
                             (H_min, S_min, V_min),
                             (H_max, S_max, V_max))
        color = colorsys.hsv_to_rgb(H_max/255, S_max/255, V_max/255)
        color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
        cv2.rectangle(frame, (320-40, 10), (320-10, 19), color=color, thickness=10)

        cv2.imshow("Original", frame)
        cv2.imshow("Thresh", thresh)
        rawCapture.truncate(0)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            print("H_min: ", H_min, "H_max: ", H_max, "S_min: ", S_min, "S_max: ", S_max, "V_min: ", V_min, "V_max: ", V_max)
            save = raw_input("Do you want to store these values in the config file? (y/n)")
            print(save)
            if save == "y":
                with open(configFile, 'r') as input_file, open('utils/new_file', 'w') as output_file:
                    for line in input_file:
                        if line.startswith("FILTER_LOWER"):
                            output_file.write('FILTER_LOWER = ({0},{1},{2})\n'.format(H_min, S_min, V_min))
                        elif line.startswith("FILTER_UPPER"):
                            output_file.write('FILTER_UPPER = ({0},{1},{2})\n'.format(H_max, S_max, V_max))
                        else:
                            output_file.write(line)
                    os.rename(configFile, configFile+"old_{0}.back".format(time.time()))
                    os.rename('utils/new_file', configFile)
                    break


if __name__ == '__main__':
    configFile = "utils/TrackerConfig.py"
    main(configFile)
