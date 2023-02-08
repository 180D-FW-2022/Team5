import json
import time

class SpeechArbitrator:
    def __init__(self,suggest):
        self.shouldSuggest = suggest
        self.powerOff = False
        self.report = False
        self.expecting_cmd = False
        self.t_last_interaction = time.time()

        #reverse the key value map because 1-to-1
        with open('speech/speechmap.json') as json_data:
            kvmap = json.loads(json_data.read())
            self.speechmap = {v: k for k, v in kvmap.items()}

    def arbitrate_speech(self,phrase_id):
        print(phrase_id)
        if (len(phrase_id) != 1):
            return
        if (self.speechmap[phrase_id] == 'hey ed '):
            # TODO: add a timeout such that when the user says hey ed, and no valid speech is detected, return to not expect cmd
            # i.e. in main routine, if t_last_interaction > threshold and expecting_cmd is true, toggle back to false
            self.expecting_cmd = True
            self.t_last_interaction = time.time()
            print("expecting speech")
            return
        if self.expecting_cmd:
            if self.speechmap[phrase_id] == 'power off ':
                print("turning off")
                self.expecting_cmd = False
                self.powerOff = True
            if self.speechmap[phrase_id] == 'stop ':
                print("Disabling suggestions")
                self.shouldSuggest = False
                self.expecting_cmd = False
            if self.speechmap[phrase_id] == 'enable ':
                print("Enabling suggestions")
                self.shouldSuggest = True
                self.expecting_cmd = False
            if self.speechmap[phrase_id] == 'report ':
                print("Providing Summary")
                self.report = True
                self.expecting_cmd = False
            self.t_last_interaction = time.time()
