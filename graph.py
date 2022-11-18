import firebase_admin
from firebase_admin import credentials, storage, db
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
from dotenv import dotenv_values
import json

# get config values and initialize firebase
config = dotenv_values(".env")
firebase_config = json.loads(config["FIREBASE"])
cred = credentials.Certificate(firebase_config)
firebase = firebase_admin.initialize_app(cred, {'databaseURL':"https://driver-s-edd-default-rtdb.firebaseio.com/"})

ref = db.reference("User1/Time/")

data = ref.get().values()
df = pd.DataFrame.from_dict(data)
# plot speed over time
ax = df.plot.bar(x='date_time', y='speed')
# plot acceleration over time
ax = df.plot.bar(x='date_time', y='acceleration')
plt.show()