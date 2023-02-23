import speech_recognition as sr
import serial
import json

class SpeechDetector():
    def __init__(self):
        with open('Team5/speech/speechmap.json') as json_data:
            self.speechmap = json.loads(json_data.read())
        self.ser = serial.Serial ("/dev/ttyS0", 9600, timeout=1)
        
    def __txToController(self,msg):
        self.ser.write(msg.encode('utf-8'))

    def detect_speech(self):
        print("Starting Speech Detection")
        r = sr.Recognizer()
        text = ""
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.non_speaking_duration = 0.3
            r.pause_threshold = 0.3
            while True:
                audio = r.listen(source, phrase_time_limit=3.0)
                try:
                    text = r.recognize_google(audio).lower()
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                    text = ""
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    text = ""
                if not text:
                    print("oops")
                    text = ""
                    continue

                print(text)
                if 'hey ed' in text:
                    self.__txToController(self.speechmap['hey ed '] + '\0')
                    text = ""
                    print("wakeword")
                if 'power off' in text:
                    self.__txToController(self.speechmap['power off '] + '\0')
                    text = ""
                    print("turning off")
                if 'stop' in text:
                    self.__txToController(self.speechmap['stop '] + '\0')
                    text = ""
                    print("Disabling suggestions")
                if 'enable' in text:
                    self.__txToController(self.speechmap['enable '] + '\0')
                    text = ""
                    print("Enabling suggestions")
                if 'report' in text:
                    self.__txToController(self.speechmap['report '] + '\0')
                    text = ""
                    print("Providing Summary")
                

s =  SpeechDetector()
s.detect_speech()