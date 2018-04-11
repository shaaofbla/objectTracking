from tracker.tracker import Tracker
from imutils.video import FPS
from TCP.client import client
import socket
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-SHOW", help="Do you want to show a preview window?", action='store_false')
parser.add_argument("-SEND2TCP", help="Do you want to establish a connection to the TCP server?", action='store_true')
parser.add_argument("-SHOW_CIRCLE", help="Do you want to draw the circle?", action='store_false')
parser.add_argument("-SHOW_PATH", help="Do you want to draw the path?", action='store_false')
parser.add_argument("-SHOW_COORDINATES", help="Do you want to show the coordinates?", action='store_false')
parser.add_argument("-SHOW_SCREEN_CENTER", help="Do you want to draw the screen center?", action='store_false')
parser.add_argument("-FLIP", help="Do you want to flip the x coordinate (get mirror image)?", action='store_true')
parser.add_argument("-MASK", help="Do you want to flip the x coordinate (get mirror image)?", action='store_true')
parser.add_argument("-FRAME", help="Do you want to flip the x coordinate (get mirror image)?", action='store_true')

args = parser.parse_args()
print args

if args.SEND2TCP:
    TCPclient = client()
    TCPclient.config()
    TCPclient.connect()

if not args.SHOW:
    args.SHOW_CIRCLE = False
    args.SHOW_PATH = False
    args.SHOW_COORDINATES = False
    args.SHOW_SCREEN_CENTER = False

print args

BallTracker = Tracker()
BallTracker.config()
BallTracker.start()

fps = FPS().start()

while True:
    try:
        BallTracker.ProcessFrame()
        BallTracker.RecordPath()
        if BallTracker.Object.Present:
            if args.FLIP:
                BallTracker.Frame = cv2.flip(BallTracker.videoStream.frame, 0)
            else:
                BallTracker.Frame = BallTracker.videoStream.frame.copy()

            if BallTracker.Object.radius > 10:
                if args.SHOW_PATH:
                    BallTracker.DrawPath()

                if args.SHOW_CIRCLE:
                    BallTracker.DrawCircle()

                if args.SEND2TCP:
                    TCPclient.sendxyr(BallTracker)
            #BallTracker.RecordPath()
                if args.SHOW_COORDINATES:
                    BallTracker.DrawCoordinates()

                if args.SHOW_SCREEN_CENTER:
                    BallTracker.DrawScreenCenter()

                if args.FRAME:
                    cv2.imshow("Frame", BallTracker.videoStream.frame)
                    print BallTracker.videoStream.frame.shape

                if args.SHOW:
                    cv2.imshow("Annotated_Frame", BallTracker.Frame)

                if args.MASK:
                    cv2.imshow("Mask", BallTracker.mask)

        key = cv2.waitKey(1) & 0xFF
        fps.update()

        if key == ord("q"):
            print key
            raise

    except KeyboardInterrupt:
        break

    except socket.error as e:
        print e
        print "[Main] Restarting client"
        TCPclient.close()
        del TCPclient
        TCPclient = client()
        TCPclient.config()
        TCPclient.connect()
        continue

fps.stop()
print "FPS: {:.2f}".format(fps.fps())
if args.SEND2TCP:
    TCPclient.close()
if args.SHOW:
    cv2.destroyAllWindows()

BallTracker.close()
del BallTracker
