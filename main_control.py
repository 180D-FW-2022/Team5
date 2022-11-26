import json
from suggest import *
from dummy import *
from firebase_rt import *
import firebase_admin
from firebase_admin import credentials, storage, db

class Main_Control:
    def __init__(self):
        with open('config.txt') as f:
            data = f.read()

        settings = json.loads(data)

        self.should_suggest = settings["enable_suggest"]
        self.user = settings["user_id"]

        self.database = Database(self.user)

        self.ref = self.database.get_ref()

    def run(self):
        while(1):
            print(self.should_suggest)

            # get current speed
            speed = curr_speed()
            acc = curr_acc()
            speedWarn = speed > 65
            self.database.uploadData(speed, acc, speedWarn)
            if speedWarn:
                warn_speed(65, round(speed,2))

            # check stop sign
            if stop_sign():
                approach_stop()

            # check gaze
            if distracted():
                driver_distracted()

            # check stop blown
            if stop_blown():
                blew_stop()




controller = Main_Control()
controller.run()