import RPi.GPIO as GPIO
import time

import sys
sys.path.append('../')

from leds.Animation import Animation

PIN_R = 25
PIN_G = 24
PIN_B = 23

# note: the animation player needs to be muiltithreaded
class AnimationPlayer:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(PIN_B,GPIO.OUT)
        GPIO.setup(PIN_G,GPIO.OUT)
        GPIO.setup(PIN_R,GPIO.OUT)

        self.playq = []
        self.current_id = 0

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
            if (len(self.playq) == 0):
                continue
            self.playAnimation()

    def queueAnimation(self, animation:Animation):
        self.playq.append(animation)

    def playAnimation(self):
        # keep this going for persistent animations
        self.playq[0].play()
        self.playq.pop()

    def dequeueAnimation(self):
        self.playq.pop()

