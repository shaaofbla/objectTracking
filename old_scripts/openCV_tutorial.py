import numpy as np
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
#Object recognition in image
"""
img_rgb = cv2.imread('picture.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

template = cv2.imread('template.jpg')
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template_width, template_height = template_gray.shape[::-1]

res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
threshold = 0.75
loc = np.where(res >= threshold)
print loc
print res

for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + template_width, pt[1] + template_height), (0,255,255), 2)

"""

#Corner recognition

img = cv2.imread('image2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)

corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = np.int0(corners)
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(img, (x,y),3,255,-1)
#cap = cv2.VideoCapture(0)


while(True):
    cv2.imshow('Detected', img)
    """
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #threshold = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 205, 1)
    lower_red = np.array([30,150,50])
    upper_red = np.array([255,255,180])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask=mask)

    edges = cv2.Canny(frame, 100,200)

    cv2.imshow('tutorial',frame)
    cv2.imshow('Edges', edges)
    """
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#cap.release()
cv2.destroyAllWindows()
