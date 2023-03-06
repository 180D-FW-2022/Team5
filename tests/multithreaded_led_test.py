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

mtr1 = MockThreadRunner(1)
runner_thread1 = threading.Thread(target=mtr1.start)
runner_thread1.start()
print("MTR1 started")

mtr2 = MockThreadRunner(2)
runner_thread2 = threading.Thread(target=mtr2.start)
runner_thread2.start()
print("MTR2 started")

mtr3 = MockThreadRunner(3)
runner_thread3 = threading.Thread(target=mtr3.start)
runner_thread3.start()
print("MTR3 started")


ap.queueAnimation(Animation(1))
time.sleep(5)
ap.queueAnimation(Animation(2))
time.sleep(5)
ap.queueAnimation(Animation(3))