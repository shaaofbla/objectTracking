from tracker.tracker import Tracker
from imutils.video import FPS
from OpenSoundControl.client import client
import cv2
import argparse

def main():
    OSCclient = client()
    OSCclient.config()

    BallTracker = Tracker()
    BallTracker.config()
    BallTracker.start()

    fps = FPS().start()

    while True:
        try:
            BallTracker.ProcessFrame()
            if BallTracker.Object.Present:
                print(BallTracker.Object.radius)
                if BallTracker.Object.radius > 0.01:
                    OSCclient.sendxyr(BallTracker)
            fps.update()

        except KeyboardInterrupt:
            break

    fps.stop()

    print("FPS: {:.2f}".format(fps.fps()))
    BallTracker.close()
    del BallTracker

def debug():
    
    OSCclient = client()
    OSCclient.config()

    BallTracker = Tracker()
    BallTracker.config()
    BallTracker.start()

    fps = FPS().start()

    while True:
        try:
            BallTracker.ProcessFrame()
            #BallTracker.RecordPath()
            
            if BallTracker.Object.Present:
                print("radius:",BallTracker.Object.radius)
                if BallTracker.Object.radius > 0.0001:
                    OSCclient.sendxyr(BallTracker)
                    print("coords:", BallTracker.Object.x, BallTracker.Object.y)
            fps.update()
            
            BallTracker.DrawScreenCenter()
            BallTracker.DrawCoordinates()
            BallTracker.DrawCircle()
            BallTracker.DrawSquare()
            
            print("showFrame")
            cv2.imshow("Frame", BallTracker.Frame)
            cv2.waitKey(1)
            
            input("Press Enter to...")
            
        except KeyboardInterrupt:
            break

    fps.stop()

    print("FPS: {:.2f}".format(fps.fps()))
    BallTracker.close()
    del BallTracker

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-DEBUG", help="run in Debug mode?", action='store_false')
    args = parser.parse_args()

    if args.DEBUG:
        print("Running...")
        main()
    else:
        print("Running in debug mode...")
        debug()
