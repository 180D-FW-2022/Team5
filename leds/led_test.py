import RPi.GPIO as GPIO
import time

PIN_R = 25
PIN_G = 24
PIN_B = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_B,GPIO.OUT)
GPIO.setup(PIN_G,GPIO.OUT)
GPIO.setup(PIN_R,GPIO.OUT)

while True:
    GPIO.output(PIN_B,GPIO.HIGH)
    time.sleep(1)

    GPIO.output(PIN_B,GPIO.LOW)
    time.sleep(1)

    GPIO.output(PIN_G,GPIO.HIGH)
    time.sleep(1)

    GPIO.output(PIN_G,GPIO.LOW)
    time.sleep(1)

    GPIO.output(PIN_R,GPIO.HIGH)
    time.sleep(1)

    GPIO.output(PIN_R,GPIO.LOW)
    time.sleep(1)

    GPIO.output(PIN_R,GPIO.HIGH)
    GPIO.output(PIN_G,GPIO.HIGH)
    time.sleep(1)

    GPIO.output(PIN_R,GPIO.LOW)
    GPIO.output(PIN_G,GPIO.LOW)
    time.sleep(1)

    GPIO.output(PIN_R,GPIO.HIGH)
    GPIO.output(PIN_B,GPIO.HIGH)
    time.sleep(1)

    GPIO.output(PIN_R,GPIO.LOW)
    GPIO.output(PIN_B,GPIO.LOW)
    time.sleep(1)

    GPIO.output(PIN_G,GPIO.HIGH)
    GPIO.output(PIN_B,GPIO.HIGH)
    time.sleep(1)

    GPIO.output(PIN_G,GPIO.LOW)
    GPIO.output(PIN_B,GPIO.LOW)
    time.sleep(1)

    GPIO.output(PIN_R,GPIO.HIGH)
    GPIO.output(PIN_G,GPIO.HIGH)
    GPIO.output(PIN_B,GPIO.HIGH)
    time.sleep(1)

    GPIO.output(PIN_R,GPIO.LOW)
    GPIO.output(PIN_G,GPIO.LOW)
    GPIO.output(PIN_B,GPIO.LOW)
    time.sleep(1)