from collections import deque
import numpy as np
import argparse
import rtmidi
import time
import imutils
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

#midi initialization
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("Virtual Port")

#arguemnt parser
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional video file")
ap.add_argument("-b", "--buffer", type = int, default = 64, help="max buffer size")
args = vars(ap.parse_args())

# defin the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
#list of tracked points

#greenLower = (29, 86, 6)
greenLower = (150, 150, 100)
#greenUpper = (64, 255, 255)
greenUpper = (255, 255, 255)
pts = deque(maxlen=args["buffer"])

#if a video path was not supplied, grap the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

#otherwise, grab a reference to the video file

else:
    camera = cv2.VideoCapture(args["video"])

previous_note_value = 0

while True:
    (grabbed, frame) = camera.read()

    if args.get("video") and not grabbed:
        break
    #resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600)
    #blurred = cv2.GaussianBlur(frame, (11,11),0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    #find contours in the maks and initialize the current (x,y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one countour was found
    class note:
       minNote = 0
       maxNote = 127
       key = 64

    class display:
        width = 600
        height = 300

    def scaleNote2displaySize(note, display):
        pass


    if len(cnts) > 0:
        #find the largest contour in the maks, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        #only proceed if the radius meets a minimum size
        if radius > 10:
            #draw the circle and centroid on the frame, then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center,5, (0,0,255), -1)
            print x, y, radius, center
        #make midi note
        note_value = int(float(x)/600*128)
        if note_value != previous_note_value:
            velocity = int(float(y)/300*128)
            note_on = [0X90, note_value, velocity]
            note_off = [0x80, note_value, 0]
            midiout.send_message(note_on)
            time.sleep(0.001)
            control =[0xb0, 0x74, velocity]
            midiout.send_message(control)
            midiout.send_message(note_off)
            previous_note_value = note_value

    #update the points queue
    pts.appendleft(center)

    #loop over the set of tracked points
    for i in xrange(1, len(pts)):
        #if either of the tracked points are None, ignore them
        if pts[i-1] is None or pts[i] is None:
            continue

        #otherwise, compute the thickness of the line and draw the conncetion lines
        thickness = int(np.sqrt(args["buffer"] /float(i + 1)) * 2.5)
        cv2.line(frame, pts[i -1], pts[i], (0, 0, 255), thickness)
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    #if key is q, stop loop
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
del midiout
