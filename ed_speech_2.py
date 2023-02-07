# from pocketsphinx import LiveSpeech
import speech_recognition as sr

class SpeechDetect():
    def __init__(self, suggest):
        self.shouldSuggest = suggest
        self.powerOff = False
        self.report = False
        r = sr.Recognizer()

    def detect_speech(self):
        expect_command = False
        print("Starting Speech Detection")
        while True:
            r = sr.Recognizer()
            text = ""
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio).lower()
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

            if not text:
                print("oops")
                continue

            print(text)

            if 'hey ed' in text:
                expect_command = True
                print(expect_command)
                continue

            if expect_command:
                if 'power off' in text:
                    print("turning off")
                    expect_command = False
                    self.powerOff = True
                if 'stop' in text:
                    print("Disabling suggestions")
                    self.shouldSuggest = False
                    expect_command = False
                if 'enable' in text:
                    print("Enabling suggestions")
                    self.shouldSuggest = True
                    expect_command = False
                if 'report' in text:
                    print("Providing Summary")
                    self.report = True
                    expect_command = False
            print(expect_command)

    def suggestSetting(self):
        return self.shouldSuggest

    def shouldPowerOff(self):
        return self.powerOff

    def shouldReport(self):
        return self.report

    def reportDone(self):
        self.report = False