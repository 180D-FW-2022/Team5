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
                return "1"
            if (step == 1):
                return "4"
            else:
                return None
            