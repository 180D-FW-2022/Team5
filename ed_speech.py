from pocketsphinx import LiveSpeech

speech = LiveSpeech(lm=False, kws="./kws.txt")

def detect_speech():
    expect_command = False
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
                expect_command = False
            if segments[0][0] == 'enable suggestions ':
                print("Enabling suggestions")
                expect_command = False
            if segments[0][0] == 'report ':
                print("Providing Summary")
                expect_command = False
        print(expect_command)

detect_speech()