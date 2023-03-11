
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
        self.session_id = str(curr_time).replace(" ", "_").replace(".", "_")

        self.ref = db.reference("devices/" + str(device_id) + "/0/sessions/" + str(self.session_id) + "/incidents")
        self.gpsref = db.reference("devices/" + str(device_id) + "/0/sessions/" + str(self.session_id) + "/gps")

        print("devices/" + str(device_id) + "/sessions/" + str(self.session_id))
    
    def get_ref(self):
        return self.ref


    def uploadData(self, speed, acc, warningType):
        curr_time = datetime.today()
        key = str(curr_time).replace(" ", "_").replace(".", "_")
        dictionary = {key: {
            "date_time": str(curr_time),
            "speed": speed,
            "acceleration": acc,
            "warning_type": warningType
        }}

        try:
            self.ref.update(dictionary)
            print("uploaded")
        except:
            print("could not upload")
            self.save_data(dictionary)

    def uploadGPS(self, lat, lon):
        curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        key = str(curr_time)
        dictionary = {
            key: {
            "lat": lat,
            "lon": lon
        }}

        try:
            self.gpsref.update(dictionary)
        except Exception as e: print(e)

    def save_data(self, dictionary):
        f = open("saved_data/" + self.session_id + ".txt", "a+")
        f.write(json.dumps(dictionary)+ "\n")
        f.close()

# while (True):
#     curr_time = datetime.today()
#     key = str(curr_time).replace(" ", "_").replace(".", "_")
#     print(key)
#     speed = random.random()*20
#     acc = random.random()*5

#     uploadData(ref, key, curr_time, speed, acc)

    
