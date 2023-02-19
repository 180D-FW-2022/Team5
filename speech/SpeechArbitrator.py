import json
import time

import sys
sys.path.append('../')

from leds.AnimationPlayer import AnimationPlayer
from leds.Animation import Animation

class SpeechArbitrator:
    def __init__(self, animationPlayer):
        self.animationPlayer = animationPlayer
        self.expecting_cmd = False
        self.t_last_interaction = time.time()

        #reverse the key value map because 1-to-1
        with open('./speech/speechmap.json') as json_data:
            kvmap = json.loads(json_data.read())
            self.speechmap = {v: k for k, v in kvmap.items()}

        print("- SpeechArbitrator Initialized")

    def arbitrate_speech(self,phrase_id):
        print(phrase_id)
        if (phrase_id == None):
            return -1
        # cooldown to exit when expecting_cmd is on for too long
        if (self.expecting_cmd == True and time.time() - self.t_last_interaction > 5):
            self.animationPlayer.clearAnimation()
            self.expecting_cmd = False
        if (self.speechmap[phrase_id] == 'hey ed '):
            # TODO: add a timeout such that when the user says hey ed, and no valid speech is detected, return to not expect cmd
            # i.e. in main routine, if t_last_interaction > threshold and expecting_cmd is true, toggle back to false
            self.expecting_cmd = True
            if (self.animationPlayer != None):
                print("Attempting to queue hey ed Animation")
                self.animationPlayer.queueAnimation(Animation(2))
            self.t_last_interaction = time.time()
            return 0

        if self.expecting_cmd:
            if self.speechmap[phrase_id] == 'power off ':
                print("turning off")
                self.t_last_interaction = time.time()
                self.expecting_cmd = False
                return 1
            if self.speechmap[phrase_id] == 'stop ':
                print("Disabling suggestions")
                self.t_last_interaction = time.time()
                self.expecting_cmd = False
                return 4
            if self.speechmap[phrase_id] == 'enable ':
                print("Enabling suggestions")
                self.t_last_interaction = time.time()
                self.expecting_cmd = False
                return 3
            if self.speechmap[phrase_id] == 'report ':
                print("Providing Summary")
                self.t_last_interaction = time.time()
                self.expecting_cmd = False
                return 2

        return 0

