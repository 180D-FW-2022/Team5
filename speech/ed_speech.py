from pocketsphinx import LiveSpeech
import serial
import json

class SpeechDetect():
    def __init__(self):
        with open('speechmap.json') as json_data:
            self.speechmap = json.loads(json_data.read())
        self.ser = serial.Serial ("/dev/ttyS0", 9600, timeout=1)
        
    def __txToController(self,msg):
        self.ser.write(msg.encode('utf-8'))

    def detect_speech(self):
        speech = LiveSpeech(lm=False, kws="./kws.txt")
        print("Starting Speech Detection")
        for phrase in speech:
            segments = phrase.segments(detailed=True)
            self.__txToController(str(segments[0][0]) +  '\0')
            print(segments[0][0])

s =  SpeechDetect()
s.detect_speech()
