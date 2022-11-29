from pocketsphinx import LiveSpeech

class SpeechDetect():
    def __init__(self, suggest):
        self.shouldSuggest = suggest

    def detect_speech(self):
        speech = LiveSpeech(lm=False, kws="./kws.txt")
        expect_command = False
        print("Starting Speech Detection")
        for phrase in speech:
            segments = phrase.segments(detailed=True)
            if segments[0][0] == 'hey ed ':
                expect_command = True
            print(segments)

            if expect_command:
                if segments[0][0] == 'power off ':
                    print("turning off")
                    expect_command = False
                if segments[0][0] == 'stop suggestions ':
                    print("Disabling suggestions")
                    self.shouldSuggest = False
                    expect_command = False
                if segments[0][0] == 'enable suggestions ':
                    print("Enabling suggestions")
                    self.shouldSuggest = True
                    expect_command = False
                if segments[0][0] == 'report ':
                    print("Providing Summary")
                    expect_command = False
            print(expect_command)

    def suggestSetting(self):
        return self.shouldSuggest