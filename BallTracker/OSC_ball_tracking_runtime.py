from tracker.tracker import Tracker
from imutils.video import FPS
from OpenSoundControl.client import client


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
            if BallTracker.Object.radius > 10:
                OSCclient.sendxyr(BallTracker)
        fps.update()

    except KeyboardInterrupt:
        break

fps.stop()

print "FPS: {:.2f}".format(fps.fps())
BallTracker.close()
del BallTracker
