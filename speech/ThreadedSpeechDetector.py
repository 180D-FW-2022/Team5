import time
import json
import speech_recognition as sr

import sys
sys.path.append('../')

from speech.StateArbitrator import StateArbitrator

class ThreadedSpeechDetector:
    def __init__(self, stateArbitrator:StateArbitrator):
        with open('./speech/speechmap.json') as json_data:
            self.speechmap = json.loads(json_data.read())
        self.stateArbitrator = stateArbitrator
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)
            self.r.non_speaking_duration = 0.3
            self.r.pause_threshold = 0.3

    def run(self):
        def callback(recognizer, audio):
            try:
                text = recognizer.recognize_google(audio)
                if (text == ""):
                    return
                text = text.lower()
                print("-- Google Speech Recognition thinks you said " + text)
                if 'hey ed' in text:
                    self.stateArbitrator.enqueue_speech(self.speechmap['hey ed '])
                elif 'power off' in text:
                    self.stateArbitrator.enqueue_speech(self.speechmap['power off '])
                elif 'stop' in text:
                    self.stateArbitrator.enqueue_speech(self.speechmap['stop '])
                elif 'enable' in text:
                    self.stateArbitrator.enqueue_speech(self.speechmap['enable '])
                elif 'report' in text:
                    self.stateArbitrator.enqueue_speech(self.speechmap['report '])
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        self.r.listen_in_background(self.m, callback)