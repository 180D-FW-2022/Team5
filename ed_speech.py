# #!/usr/bin/env python3

# # NOTE: this example requires PyAudio because it uses the Microphone class

# import speech_recognition as sr

# # obtain audio from the microphone
# r = sr.Recognizer()
# # with sr.Microphone() as source:
# #     # r.adjust_for_ambient_noise(source, duration=5)
# #     print("Say something!")
# #     audio = r.listen(source)

# # # recognize speech using Google Speech Recognition
# # try:
# #     # for testing purposes, we're just using the default API key
# #     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
# #     # instead of `r.recognize_google(audio)`
# #     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
# # except sr.UnknownValueError:
# #     print("Google Speech Recognition could not understand audio")
# # except sr.RequestError as e:
# #     print("Could not request results from Google Speech Recognition service; {0}".format(e))

# while True:
#     with sr.Microphone() as source:
#         audio = r.listen(source)

#         # recognize speech using Google Speech Recognition
#     try:
#         # for testing purposes, we're just using the default API key
#         # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#         # instead of `r.recognize_google(audio)`
#         print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
# import os
# from pocketsphinx import LiveSpeech, get_model_path

# model_path = get_model_path()

# speech = LiveSpeech(
#     verbose=False,
#     sampling_rate=16000,
#     buffer_size=2048,
#     no_search=False,
#     full_utt=False,
#     hmm=os.path.join(model_path, 'en-us'),
#     lm=os.path.join(model_path, 'en-us.lm.bin'),
#     dic=os.path.join(model_path, 'cmudict-en-us.dict')
# )

# for phrase in speech:
#     print(phrase)

from pocketsphinx import LiveSpeech

speech = LiveSpeech(lm=False, kws="./kws.txt")
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
    print(expect_command)