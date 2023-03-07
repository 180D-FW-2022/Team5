import speech_recognition as sr
import json
import time

class SpeechDetector():
    def __init__(self):
        self.r = sr.Recognizer()

        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            self.r.non_speaking_duration = 0.26
            self.r.pause_threshold = 0.26

    def detect_speech(self, source):
        t0 = time.time()

        print("Starting Speech Detection")
        text = ""
        while True:
                print("listening...")
                audio = self.r.listen(source, phrase_time_limit=2.5)
                print("Done. Sending to API...")
                try:
                    text = self.r.recognize_google(audio).lower()
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

                if text != "":
                    print(text)
                    break
                # more than 5 seconds listening
                if time.time() - t0 > 2.5:
                    break

                '''
                if 'hey ed' in text:
                    text = ""
                    print("wakeword")
                if 'power off' in text:
                    text = ""
                    print("turning off")
                if 'stop' in text:
                    text = ""
                    print("Disabling suggestions")
                if 'enable' in text:
                    text = ""
                    print("Enabling suggestions")
                if 'report' in text:
                    text = ""
                    print("Providing Summary")
                '''
                
if __name__ == '__main__':
    s =  SpeechDetector()
    s.detect_speech()
