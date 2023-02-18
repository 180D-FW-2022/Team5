import RPi.GPIO as GPIO
import time

PIN_R = 25
PIN_G = 24
PIN_B = 23

class Animation:
    def __init__(self, id:int):
        self.id = id
        self.persistent = False
        self.currently_playing = False
        self.finished = False

    def play(self):
        print("Actually playing animation " + str(self.id))
        if self.id == 0:
            self.currently_playing = False
        elif self.id == 1: 
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
            self.finished = True
            return
        elif self.id == 2:
            self.currently_playing = True
            self.current_id = 2
            self.persistent = True
            GPIO.output(PIN_G,GPIO.HIGH)
            GPIO.output(PIN_B,GPIO.HIGH)
        elif self.id == 3:
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
            self.finished = True
            return
        elif self.id == 4:
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
            self.finished = True
            return
        