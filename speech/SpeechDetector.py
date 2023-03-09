import speech_recognition as sr
import json
import time

class SpeechDetector():
    def __init__(self, stateArbitrator=None):
        self.stateArbitrator = stateArbitrator
        try:
            with open('./speech/speechmap.json') as json_data:
                self.speechmap = json.loads(json_data.read())
        except:
            print("WARNING: './speech/speechmap.json' was not found. No speechmap initialized, continuing anyway without it and initializing self.stateArbitrator to None")
            self.stateArbitrator = None

        if self.stateArbitrator is None:
            print("WARNING: state_arbitrator in hotkey.py was not passed to PorcupineDemo object or './speech/speechmap.json not found'. Not interfacing with LEDs or main_control.py at all...")

        self.r = sr.Recognizer()

        with sr.Microphone(2) as source:
            self.r.adjust_for_ambient_noise(source)
            self.r.non_speaking_duration = 0.26
            self.r.pause_threshold = 0.26

    def parse_text(self, text):
        if self.stateArbitrator is None:
            return False

        if 'power off' in text:
            self.stateArbitrator.enqueue_speech(self.speechmap['power off '])
            print("turning off...")
        if 'stop' in text:
            self.stateArbitrator.enqueue_speech(self.speechmap['stop '])
            print("Disabling suggestions...")
        if 'enable' in text:
            self.stateArbitrator.enqueue_speech(self.speechmap['enable '])
            print("Enabling suggestions...")
        if 'report' in text:
            self.stateArbitrator.enqueue_speech(self.speechmap['report '])
            print("Providing Summary...")

        return True

    def detect_speech(self, source=None):
        t0 = time.time()
        if self.stateArbitrator is not None:
            # function is only run when 'hey edd' is detected
            self.stateArbitrator.enqueue_speech(self.speechmap['hey ed '])

        print("Starting Speech Detection")
        text = ""
        while True:
            with sr.Microphone(2) as source:
                print("listening...")
                audio = self.r.listen(source, phrase_time_limit=2.5)
                print("Done. Sending to API...")
                try:
                    text = self.r.recognize_google(audio).lower()
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

                if text != "":
                    print(text)
                    # check keyword to break out of listening incase of mistake
                    if "never mind" in text:
                        return
                    self.parse_text(text)
                    break

                # more than 3 seconds listening
                if time.time() - t0 > 3:
                    break

                
if __name__ == '__main__':
    s =  SpeechDetector()
    s.detect_speech()
