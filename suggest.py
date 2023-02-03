import pyttsx3
import threading
import queue
import time

class Suggest():
    def __init__():
        self.engine = pyttsx3.init()
        self.q = queue.Queue()

        self.runner = threading.Thread(target=self.__run)
        self.runner.start()

    def __run(self):
        while True:
            if not self.q.empty():
                text = q.get()
                engine.say(text)
                engine.runAndWait()
            time.sleep(0.05)


    def approach_stop(self):
        self.q.put("Approaching stop sign. Start slowing down!")

    def warn_speed(self, limit, speed):
        self.q.put("Slow down! Speed limit is " + str(limit) + "mph. Your speed is " + str(speed) + "mph.")

    def blew_stop(self):
        self.q.put("Start slowing down sooner next time")

    def driver_distracted(self):
        self.q.put("Keep your eyes on the road!")

    def disable_suggestions(self):
        self.q.put("Suggestions disabled")

    def enable_suggestions(self):
        self.q.put("Suggestions enabled")

    def power_off(self):
        self.q.put("Ending session")

    def say_phrase(self, text):
        self.q.put(text)
