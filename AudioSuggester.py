import pyttsx3
import queue
import time

class AudioSuggester():
    def __init__(self, should_suggest:bool):
        self.engine = pyttsx3.init()
        self.q = queue.Queue()
        self.should_suggest = should_suggest
        print("- AudioSuggester Initialized")

    def run(self):
        while True:
            if not self.q.empty():
                text = self.q.get()
                self.engine.say(text)
                self.engine.runAndWait()
            time.sleep(0.1)

    def approach_stop(self):
        if self.should_suggest:
            self.q.put("Approaching stop sign. Start slowing down!")

    def warn_speed(self, limit, speed):
        if self.should_suggest:
            self.q.put("Slow down! Speed limit is " + str(limit) + "mph. Your speed is " + str(speed) + "mph.")

    def slow_down(self):
        if self.should_suggest:
            self.q.put("Slow Down!")

    def aggressive(self):
        if self.should_suggest:
            self.q.put("Don't be so aggressive")

    def blew_stop(self):
        if self.should_suggest:
            self.q.put("Start slowing down sooner next time")

    def driver_distracted(self):
        if self.should_suggest:
            self.q.put("Keep your eyes on the road!")

    def disable_suggestions(self):
        self.q.put("Suggestions disabled")

    def enable_suggestions(self):
        self.q.put("Suggestions enabled")

    def power_off(self):
        self.q.put("Ending session")

    def say_phrase(self, text):
        self.q.put(text)

    def calibration_successful(self):
        self.q.put("Calibration successful")

    def report(self,incident_summary:dict):
        report_text = "This session, You have had "
        for inc in incident_summary:
            report_text += str(incident_summary[inc])
            report_text += " "
            report_text += inc
            report_text += "incidents, "
        self.q.put(report_text)