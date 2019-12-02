import utils.TrackerConfig as config

from pythonosc import udp_client


class client:
    def __init__(self):
        self.name = "Name not set properly"

    def config(self):
        self.name = config.NAME
        print("Name of Camera: ", self.name)
        #self.client.connect((config.OSC_IP, config.OSC_PORT))
        self.client = udp_client.SimpleUDPClient(
            config.OSC_IP, config.OSC_PORT)
        print("connecting to {} on port {}".format(config.OSC_IP, config.OSC_PORT))

    def send(self, message):
        oscmsgAddress = '/{}'.format(self.name)
        self.client.send_message(oscmsgAddress, message)

    def sendxyr(self, tracker):
        x = tracker.Object.x
        y = tracker.Object.y
        r = tracker.Object.radius
        message = "{:.3f}\t{:.3f}\t{:.3f}\t\n".format(x, y, r)
        self.send(message)
