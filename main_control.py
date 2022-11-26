import json
from suggest import *
from dummy import *
from firebase_rt import *
from ed_speech import SpeechDetect
import firebase_admin
from firebase_admin import credentials, storage, db
import threading

class Main_Control:
    def __init__(self):
        with open('config.txt') as f:
            data = f.read()
            f.close()

        settings = json.loads(data)

        self.should_suggest = settings["enable_suggest"]
        self.user = settings["user_id"]

        self.database = Database(self.user)
        self.speech = SpeechDetect(self.should_suggest)

        self.ref = self.database.get_ref()

    def change_config(self):
        f = open('config.txt', "w")
        dictionary = {"user_id": self.user, "enable_suggest": self.should_suggest}
        f.write(json.dumps(dictionary))
        f.close()

    def run(self):
        suggest = True
        t1 = threading.Thread(target=self.speech.detect_speech, daemon=True)
        t1.start()
        while(1):
            # check if we should provide audio suggestions
            should = self.speech.suggestSetting()

            # update config if settings changed
            if should != self.should_suggest:
                self.should_suggest = should
                self.change_config()

            # get current speed
            speed = curr_speed()
            acc = curr_acc()
            speedWarn = speed > 65
            self.database.uploadData(speed, acc, speedWarn)
            if self.should_suggest and speedWarn:
                warn_speed(65, round(speed,2))

            # check stop sign
            if self.should_suggest and stop_sign():
                approach_stop()

            # check gaze
            if self.should_suggest and distracted():
                driver_distracted()

            # check stop blown
            if self.should_suggest and stop_blown():
                blew_stop()




controller = Main_Control()
controller.run()