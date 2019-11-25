import OSC
import utils.TrackerConfig as config


class client:
    def __init__(self):
        self.name = "Name not set properly"
        self.client = OSC.OSCClient()

    def config(self):
        self.name = config.NAME
        print("Name of Camera: ", self.name)
        self.client.connect((config.OSC_IP, config.OSC_PORT))
        print("connecting to {} on port {}".format(config.OSC_IP, config.OSC_PORT))

    def send(self, message):
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress('/{}'.format(self.name))
        oscmsg.append(message)
        self.client.send(oscmsg)

    def sendxyr(self, tracker):
        x = tracker.Object.x
        y = tracker.Object.y
        r = tracker.Object.radius
        message = "{:.2f}\t{:.2f}\t{:.2f}\t\n".format(x, y, r)
        self.send(message)
