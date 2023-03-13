import RPi.GPIO as GPIO
import board
import neopixel
import time
import threading

NEOPIXEL_PIN = board.D10
NUM_PIXELS = 24
ORDER = neopixel.GRB

class Animation:
    def __init__(self, id:int):
        self.pixels = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=True, pixel_order=ORDER)
        self.id = id
        self.persistent = False
        self.currently_playing = False
        self.finished = False

    def play(self):
        print("Actually playing animation: " +  str(self.id))
        lock = threading.Lock()
        lock.acquire()
        if self.id == 0:
            self.reset()
            self.currently_playing = False
        elif self.id == 1:
            self.animation_deviceOn()
        elif self.id == 2:
            self.animation_eddListening()
        elif self.id == 3:
            self.animation_suggestionsOn()
        elif self.id == 4:
            self.animation_suggestionsOff()
        elif self.id == 5:
            self.animation_calibrate()
        elif self.id == 6:
            self.animation_report()
        lock.release()

    def reset(self):
        self.pixels.fill((0, 0, 0))
        
    def animation_deviceOn(self):
        self.reset()
        self.currently_playing = True
        self.current_id = 1
        self.pixels.fill((0,100,0))
        time.sleep(0.5)
        self.pixels.fill((0,0,0))
        time.sleep(0.5)
        self.pixels.fill((0,100,0))
        time.sleep(0.5)
        self.pixels.fill((0,0,0))
        self.reset()
        self.currently_playing = False
        self.finished = True

    def animation_eddListening(self):
        self.reset()
        self.currently_playing = True
        self.current_id = 2
        self.persistent = True
        self.pixels.fill((0,100,100))

    def animation_suggestionsOn(self):
        self.reset()
        self.currently_playing = True
        self.current_id = 3
        self.pixels.fill((100,100,0))
        time.sleep(0.25)
        self.pixels.fill((0,0,0))
        time.sleep(0.25)
        self.pixels.fill((100,100,0))
        time.sleep(0.25)
        self.pixels.fill((0,0,0))
        time.sleep(0.25)
        self.pixels.fill((100,100,0))
        time.sleep(0.25)
        self.pixels.fill((0,0,0))
        self.reset()
        self.currently_playing = False
        self.finished = True

    def animation_suggestionsOff(self):
        self.reset()
        self.currently_playing = True
        self.current_id = 4
        self.pixels.fill((100,0,0))
        time.sleep(0.25)
        self.pixels.fill((0,0,0))
        time.sleep(0.25)
        self.pixels.fill((100,0,0))
        time.sleep(0.25)
        self.pixels.fill((0,0,0))
        time.sleep(0.25)
        self.pixels.fill((100,0,0))
        time.sleep(0.25)
        self.pixels.fill((0,0,0))
        self.reset()
        self.currently_playing = False
        self.finished = True

    def animation_calibrate(self):
        self.reset()
        self.currently_playing = True
        self.current_id = 5
        for i in range(0,NUM_PIXELS):
            self.pixels[i] = (100,50,0)
            time.sleep(0.05)
        for i in range(0,NUM_PIXELS):
            self.pixels[i] = (0,0,0)
            time.sleep(0.05)
        self.reset()
        self.currently_playing = False
        self.finished = True

    def animation_report(self):
        self.reset()
        self.currently_playing = True
        self.current_id = 6
        for i in range(0,NUM_PIXELS):
            self.pixels[i] = (100,100,100d)
            time.sleep(0.05)
        for i in range(0,NUM_PIXELS):
            self.pixels[i] = (0,0,0)
            time.sleep(0.05)
        self.reset()
        self.currently_playing = False
        self.finished = True

if __name__ == "__main__":
    a1 = Animation(1)
    a1.play()
    time.sleep(3)
    a2 = Animation(2)
    a2.play()
    time.sleep(3)
    a3 = Animation(3)
    a3.play()
    time.sleep(3)
    a4 = Animation(4)
    a4.play()
    time.sleep(3)
    a5 = Animation(5)
    a5.play()
    time.sleep(3)
    a6= Animation(6)
    a6.play()
    time.sleep(3)