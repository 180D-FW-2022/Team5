import threading
import time
import sys
sys.path.append('../')

from leds.AnimationPlayer import AnimationPlayer
from leds.Animation import Animation
from mock.MockThreadRunner import MockThreadRunner

ap = AnimationPlayer()
led_thread = threading.Thread(target=ap.play)
led_thread.start()
print("LED Thread started")

mtr = MockThreadRunner()
runner_thread = threading.Thread(target=mtr.start)
runner_thread.start()
print("MTR started")

ap.queueAnimation(Animation(1))
time.sleep(5)
ap.queueAnimation(Animation(2))
time.sleep(5)
ap.queueAnimation(Animation(3))