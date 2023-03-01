import threading

import sys
sys.path.append('../')

from leds.AnimationPlayer import AnimationPlayer
from leds.Animation import Animation

ap = AnimationPlayer()
led_thread = threading.Thread(target=ap.play)
led_thread.start()
print("LED Thread started")

ap.queueAnimation(Animation(1))
ap.queueAnimation(Animation(2))
ap.queueAnimation(Animation(3))