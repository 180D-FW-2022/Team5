
import firebase_admin
from firebase_admin import credentials, storage, db
from datetime import datetime
import random
from dotenv import dotenv_values
import json

class Database:
    def __init__(self, device_id):
        # get config values and initialize firebase
        config = dotenv_values(".env")
        firebase_config = json.loads(config["FIREBASE"])
        cred = credentials.Certificate(firebase_config)
        firebase = firebase_admin.initialize_app(cred, {'databaseURL':"https://driver-s-edd-default-rtdb.firebaseio.com/"})

        curr_time = datetime.today()
        session_id = str(curr_time).replace(" ", "_").replace(".", "_")

        self.ref = db.reference("devices/" + str(device_id) + "/sessions/" + str(session_id) + "/incidents")

        print("devices/" + str(device_id) + "/sessions/" + str(session_id))
    
    def get_ref(self):
        return self.ref


    def uploadData(self, speed, acc, warningType):
        curr_time = datetime.today()
        key = str(curr_time).replace(" ", "_").replace(".", "_")

        self.ref.update({key: {
            "date_time": str(curr_time),
            "speed": speed,
            "acceleration": acc,
            "warning_type": warningType
        }})
        print("uploaded")

# while (True):
#     curr_time = datetime.today()
#     key = str(curr_time).replace(" ", "_").replace(".", "_")
#     print(key)
#     speed = random.random()*20
#     acc = random.random()*5

#     uploadData(ref, key, curr_time, speed, acc)

    
