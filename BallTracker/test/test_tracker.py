from tracker.tracker import Tracker
import unittest
import time
import numpy as np

class TestTracker(unittest.TestCase):

    def test_get_frame_without_startStream(self):
        testTracker = Tracker(lower =(0,0,0),upper=(255,255,255))
        frame = testTracker.videoStream.read()
        self.assertIsNone(frame)
        testTracker.close()
        del testTracker

    @unittest.skip("not working")
    def test_start_piVideoStream(self):
        testTracker = Tracker(lower =(0,0,0),upper=(255,255,255))
        testTracker.start()
        frame = testTracker.videoStream.read()
        frameShape = np.shape(frame)
        expectedFrameShape = (testTracker.Resolution[1],testTracker.Resolution[0],3)
        self.assertEqual(frameShape,expectedFrameShape)
        testTracker.close()

    def test_piVideoStream_closed(self):
        testTracker = Tracker(lower =(0,0,0),upper=(255,255,255))
        testTracker.start()
        testTracker.videoStream.read()
        testTracker.close()
        frame = testTracker.videoStream.read()
        self.assertIsNone(frame)
        del testTracker

