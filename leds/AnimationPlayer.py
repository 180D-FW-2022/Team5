import RPi.GPIO as GPIO
import time

import sys
sys.path.append('../')

from leds.Animation import Animation

# note: the animation player needs to be muiltithreaded
class AnimationPlayer:
    def __init__(self):
        self.playq = []
        self.current_id = 0
        print("- AnimationPlayer Initialized")

    '''
        animation IDs correspond to states of Edd
        0: No animation playing
        1: bootup complete - green blink twice
        2: active ready (hey edd detected) - aqua turns on 
        3: enable suggestions - yellow blink twice
        4: stop suggestions - red blink twice
        
        cases to consider:
        - active read timeout (hey edd detected but command not uttered after timeout t) - go to state 0
    '''

    def play(self):
        while (True):
            if (len(self.playq) != 0):
                self.playAnimation()
            time.sleep(0.1)

    def queueAnimation(self, animation:Animation):
        self.playq.append(animation)

    def playAnimation(self):
        # keep this going for persistent animations
        self.playq[0].play()
        self.playq.pop()

    def clearAnimation(self):
        if (len(self.playq) > 0):
            self.playq.pop()
        else:
            self.queueAnimation(Animation(0))

