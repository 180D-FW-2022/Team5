import RPi.GPIO as GPIO
import time

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

        self.currently_playing = False
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
    def play(self, action:int):
        if action == 0:
            self.currently_playing = False
            self.current_id = 0
        elif action == 1: 
            self.currently_playing = True
            self.current_id = 1
            GPIO.output(PIN_G,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(PIN_G,GPIO.LOW)
            time.sleep(1)
            GPIO.output(PIN_G,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(PIN_G,GPIO.LOW)
            self.currently_playing = False
            self.current_id = 0
        elif action == 2:
            self.currently_playing = True
            self.current_id = 2
            GPIO.output(PIN_G,GPIO.HIGH)
            GPIO.output(PIN_B,GPIO.HIGH)
        elif action == 3:
            self.currently_playing = True
            self.current_id = 3
            GPIO.output(PIN_G,GPIO.HIGH)
            GPIO.output(PIN_R,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(PIN_G,GPIO.LOW)
            GPIO.output(PIN_R,GPIO.LOW)
            time.sleep(1)
            GPIO.output(PIN_G,GPIO.HIGH)
            GPIO.output(PIN_R,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(PIN_G,GPIO.LOW)
            GPIO.output(PIN_R,GPIO.LOW)
            self.currently_playing = False
            self.current_id = 0
        elif action == 4:
            self.currently_playing = True
            self.current_id = 4
            GPIO.output(PIN_R,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(PIN_R,GPIO.LOW)
            time.sleep(1)
            GPIO.output(PIN_R,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(PIN_R,GPIO.LOW)
            self.currently_playing = False
            self.current_id = 0

