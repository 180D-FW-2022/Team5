import pyttsx3

engine = pyttsx3.init()

def approach_stop():
    text = "Approaching stop sign. Start slowing down!"
    engine.say(text)
    engine.runAndWait()

def warn_speed(limit, speed):
    text = "Slow down! Speed limit is " + str(limit) + "mph. Your speed is " + str(speed) + "mph."
    engine.say(text)
    engine.runAndWait()

def blew_stop():
    text = "Start slowing down sooner next time"
    engine.say(text)
    engine.runAndWait()

def driver_distracted():
    text = "Keep your eyes on the road!"
    engine.say(text)
    engine.runAndWait()

def driver_tired():
    text = "You are tired!"
    engine.say(text)
    engine.runAndWait()

def disable_suggestions():
    text = "Suggestions disabled"
    engine.say(text)
    engine.runAndWait()

def enable_suggestions():
    text = "Suggestions enabled"
    engine.say(text)
    engine.runAndWait()

def power_off():
    text = "Ending session"
    engine.say(text)
    engine.runAndWait()

def say_phrase(text):
    engine.say(text)
    engine.runAndWait()
