from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread


class PiVideoStream:
    def __init__(self,
                 awb_mode = "sunlight",
                 iso = 400,
                 resolution=(320, 240),
                 shutter_speed = 1000,
                 framerate=32):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.shutter_speed = shutter_speed
        self.camera.ISO = iso
        self.exposure_mode = 'off'
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="bgr",
                                                     use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def close(self):
        try:
            self.stream.close()
        except ValueError:
            pass
        try:
            self.rawCapture.close()
        except ValueError:
            pass
        try:
            self.camera.close()
        except ValueError:
            pass
        self.frame = None

    def update(self):
        for f in self.stream:
            self.frame = f.array
            self.rawCapture.truncate(0)

            if self.stopped:
                self.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

if __name__ == "__main__":
    
    import cv2
    import time
    from TrackerConfig import *
    
    print("awb Mode: ", CAMERA_AWB_MODE)
    print("shutterspeed: ",CAMERA_SHUTTERSPEED)
    print("resolution: ", CAMERA_RESOLUTION)
    print("iso: ", CAMERA_ISO)
    print("framerate: ", CAMERA_FRAMERATE)
    stream = PiVideoStream(resolution = CAMERA_RESOLUTION,
                           framerate = CAMERA_FRAMERATE,
                           shutter_speed = CAMERA_SHUTTERSPEED,
                           iso = CAMERA_ISO,
                           awb_mode = CAMERA_AWB_MODE)
    stream.start()
    time.sleep(2)
    
    while True:
        cv2.imshow("frame", stream.read())
        key = cv2.waitKey(1)
        if key == 27:
            break
        