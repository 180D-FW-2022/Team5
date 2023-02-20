import time
import json
import speech_recognition as sr

import sys
sys.path.append('../')

class ThreadedSpeechDetector:
    def __init__(self):
        with open('./speech/speechmap.json') as json_data:
            self.speechmap = json.loads(json_data.read())
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)
            self.r.non_speaking_duration = 0.3
            self.r.pause_threshold = 0.3

    def callback(self, audio):
        try:
            print("Google Speech Recognition thinks you said " + self.r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def run(self):
        stop_listening = self.r.listen_in_background(self.m,self.callback)