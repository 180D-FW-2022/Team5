import threading

from comms.TCPReceiver import TCPReceiver
from leds.AnimationPlayer import AnimationPlayer
from leds.Animation import Animation

tcpr = TCPReceiver()
ap = AnimationPlayer()

led_thread = threading.Thread(target=ap.play)
led_thread.start()
print("LED Thread started")

while (True):
    conn = tcpr.run()
    while (True):
        tcpr.interpret(conn)
        ap.queueAnimation(Animation(tcpr.recq[0]))
        tcpr.recq.pop()
    