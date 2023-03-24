import json
import time
import threading
import queue

import sys
sys.path.append('../')

from leds.AnimationSender import AnimationSender
from AudioSuggester import AudioSuggester

class StateArbitrator:
    def __init__(self, animationSender:AnimationSender, audioSuggester:AudioSuggester, calibration_queue:queue.Queue):
        self.animationSender = animationSender
        self.audioSuggester = audioSuggester
        self.expecting_cmd = False
        self.t_last_interaction = time.time()

        self.incident_summary = dict()
        self.speech_queue = []

        self.calib_q = calibration_queue

        self.incident_summary_lock = threading.Lock()

        #reverse the key value map because 1-to-1
        with open('./speech/speechmap.json') as json_data:
            kvmap = json.loads(json_data.read())
            self.speechmap = {v: k for k, v in kvmap.items()}

        print("- SpeechArbitrator Initialized")

    def enqueue_speech(self, phrase_id):
        self.speech_queue.append(phrase_id)

    def arbitrate_speech(self,phrase_id):
        print(phrase_id)
        if (phrase_id == None):
            return -1
        # cooldown to exit when expecting_cmd is on for too long
        if (self.speechmap[phrase_id] == 'hey ed '):
            # TODO: add a timeout such that when the user says hey ed, and no valid speech is detected, return to not expect cmd
            # i.e. in main routine, if t_last_interaction > threshold and expecting_cmd is true, toggle back to false
            self.expecting_cmd = True
            if (self.animationSender != None):
                print("Attempting to queue hey ed Animation")
                self.animationSender.queueSend(2)
            self.t_last_interaction = time.time()
            return 0

        if self.expecting_cmd:
            if self.speechmap[phrase_id] == 'power off ':
                self.expecting_cmd = False
                print("turning off")
                self.t_last_interaction = time.time()
                return 1
            if self.speechmap[phrase_id] == 'stop ':
                self.expecting_cmd = False
                print("Disabling suggestions")
                self.audioSuggester.should_suggest = False
                self.animationSender.queueSend(4) # Disable Suggestions Animation (ID = 4)
                self.audioSuggester.disable_suggestions()
                print("Attempting to queue stopping animation")
                return 4
            if self.speechmap[phrase_id] == 'enable ':
                self.expecting_cmd = False
                print("Enabling suggestions")
                self.audioSuggester.should_suggest = True
                self.animationSender.queueSend(3) # Enable suggestions Animation (ID = 3)
                self.audioSuggester.enable_suggestions()
                print("Attempting to queue enable animation")
                self.t_last_interaction = time.time()
                return 3
            if self.speechmap[phrase_id] == 'report ':
                self.expecting_cmd = False
                print("Providing Summary")

                self.incident_summary_lock.acquire()
                cur_incident_summary = self.incident_summary
                self.incident_summary_lock.release()
                self.animationSender.queueSend(6)
                self.audioSuggester.report(cur_incident_summary)
                self.t_last_interaction = time.time()
                return 2
            if (self.speechmap[phrase_id] == 'calibrate '):
                self.expecting_cmd = False
                print("Calibration in progress")

                self.calib_q.put(1)
                self.animationSender.queueSend(5)
                self.audioSuggester.calibration_successful()
                self.t_last_interaction = time.time()

        return 0

    def loop_state_updater(self):
        if (self.expecting_cmd == True and time.time() - self.t_last_interaction > 10):
            self.animationSender.queueSend(0)
            self.expecting_cmd = False
        if (len(self.speech_queue) != 0):
            print("Arbitrating speech_queue item " +str(self.speech_queue[0]))
            self.arbitrate_speech(self.speech_queue[0])
            self.speech_queue.pop()
        time.sleep(0.05)
        
