import time

import sys
sys.path.append('../')

from comms.TCPSender import TCPSender

ADDR = "192.168.222.96"

class AnimationSender:
    def __init__(self):
        self.tcpSender = TCPSender(ADDR, True)
        self.sendq = []

    def queueSend(self, animation:int):
        self.sendq.append(str(animation))

    def start(self):
        while (True):
            if (len(self.sendq) != 0):
                self.tcpSender.send(self.sendq[0])
                self.sendq.pop()
            time.sleep(0.1)