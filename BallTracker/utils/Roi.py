class Roi():
    def __init__(self):
        self.x = None
        self.y = None
        self.x2 = None
        self.y2 = None
        self.w = None
        self.h = None

def fold(val, min, max):
    if val >= min and val <=max:
        return(val)
    elif val < min:
        return(min)
    elif val > max:
        return max
    else:
        print("oops")
        