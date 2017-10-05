from collections import deque
import numpy as np
import time
import imutils
import sys
import cv2


#list of tracked points

#greenLower = (29, 86, 6)
greenLower = (41, 165, 52)
#greenUpper = (64, 255, 255)
greenUpper = (105, 255, 255)

pts = deque()

camera = cv2.VideoCapture(0)

#otherwise, grab a reference to the video file


previous_note_value = 0

while True:
    (grabbed, frame) = camera.read()

    if not grabbed:
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


    if len(cnts) > 0:
        #find the largest contour in the maks, then use it to compute the minimum enclosing circle and centroid
        #c = max(cnts, key=cv2.contourArea)
        #((x,y),radius) = cv2.minEnclosingCircle(c)
        #M = cv2.moments(c)
        #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        for i in xrange(len(cnts)):
            cntsArea = cv2.contourArea(cnts[i])
            if cntsArea > 700:
                cv2.drawContours(frame, cnts,i,(0,0,255))
                print cntsArea

            #print len(cnts[i]), "\t",np.mean(cnts[i]),"\t", np.var(cnts[i]), "\t",np.mean(cnts[i],axis=0)[0][0],"\t",np.mean(cnts[i],axis=0)[0][1]

            #print np.var(cnts[i],axis=0)[0], np.var(cnts[i], axis=0)[1]
        #only proceed if the radius meets a minimum size
        #if radius > 10:
            #draw the circle and centroid on the frame, then update the list of tracked points
            #cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            #cv2.circle(frame, center,5, (0,0,255), -1)
            #print x, y, radius, center
        #    pass
    #update the points queue
    #pts.appendleft(center)


    #loop over the set of tracked points
    """
    for i in xrange(1, len(pts)):
        #if either of the tracked points are None, ignore them
        if pts[i-1] is None or pts[i] is None:
            continue

        #otherwise, compute the thickness of the line and draw the conncetion lines
        thickness = int(np.sqrt(64 /float(i + 1)) * 2.5)
        cv2.line(frame, pts[i -1], pts[i], (0, 0, 255), thickness)
    """
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    #if key is q, stop loop
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
s.close()
