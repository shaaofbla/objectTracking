#from __future__ import division
import numpy as np
import sys
import rtmidi
import time
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("Virtual Por")

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
previous_note_value = 0
while 1:
    start_time = time.time()
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0),2)
        note_value = int(float(x)/1080*128)
        if note_value != previous_note_value:
            control_change = [0xb0,0x74,int(float(y)/720*12)]
            midiout.send_message(control_change)
            face_surface = w*h
            max_surface = 1080*720
            min_surface = 1
            face_surface_to_midi_range = int(float(face_surface)/max_surface*128)
            velocity = face_surface_to_midi_range
            print velocity
            note_on = [0x90, note_value, velocity]
            note_off = [0x80, note_value, 0]
            midiout.send_message(note_on)
            time.sleep(0.01)
            midiout.send_message(note_off)
            """
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0, 255,0),2)
            """
            previous_note_value = note_value
        else:
            next
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    elapsed_time = time.time() - start_time
    print elapsed_time
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
del midiout
