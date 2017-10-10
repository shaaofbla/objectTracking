from collections import deque


class Object():
    def __init__(self):
        self.x = None
        self.y = None
        self.radius = None
        self.Moments = None
        self.Center = None
        self.Path_length = 64
        self.Path = deque(maxlen = self.Path_length)

    def PathAppendPoint(self,point):
        self.Path.appendleft(point)
        return
