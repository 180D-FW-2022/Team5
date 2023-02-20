import time
import sys
sys.path.append('../')

class MockSpeechDetector:
    def __init__(self, scheme:int):
        self.scheme = scheme

    def run_mock_speech_detector(self, step:int):
        print("Running scheme " + str(self.scheme) + " of MOCK SPEECH DETECTOR")
        if (self.scheme == 1):
            if (step == 0):
                time.sleep(3)
                return "1" # HEY ED! light up
            if (step == 1):
                time.sleep(3)
                return "4" # ENABLE! light up
            if (step == 2):
                time.sleep(3)
                return "3" # STOP! no light, due to no "hey ed" utterance
            if (step == 3):
                time.sleep(3)
                return "1" # HEY ED! light up
            if (step == 4):
                time.sleep(3)
                return "3" # STOP! light up
            if (step == 5):
                time.sleep(3)
                return "1" # HEY ED! light up, light turns off in 5s due to timeout
            if (step == 6):
                time.sleep(8)
                return "4" # ENABLE! no light, due to timeout
            else:
                return None
            