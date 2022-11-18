
import firebase_admin
from firebase_admin import credentials, storage, db
from datetime import datetime
import random
from dotenv import dotenv_values
import json


def uploadData(ref, key, curr_time, speed, acc):
    ref.update({key: {
        "date_time": str(curr_time),
        "speed": speed,
        "acceleration": acc,
        "speed_warning": False
    }})


# get config values and initialize firebase
config = dotenv_values(".env")
firebase_config = json.loads(config["FIREBASE"])
cred = credentials.Certificate(firebase_config)
firebase = firebase_admin.initialize_app(cred, {'databaseURL':"https://driver-s-edd-default-rtdb.firebaseio.com/"})

ref = db.reference("User1/Time/")

while (True):
    curr_time = datetime.today()
    key = str(curr_time).replace(" ", "_").replace(".", "_")
    print(key)
    speed = random.random()*20
    acc = random.random()*5

    uploadData(ref, key, curr_time, speed, acc)

    
