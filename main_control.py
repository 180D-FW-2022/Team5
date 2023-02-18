import json
import sys
import time

from suggest import *
from dummy import *
from firebase_rt import *
from firebase_admin import credentials, storage, db

import threading
import comms.uart_proc as uart_utils
import comms.uart_rec as uart_receiver

from leds.AnimationPlayer import AnimationPlayer
from leds.Animation import Animation
from speech.SpeechArbitrator import SpeechArbitrator

class Main_Control:
    def __init__(self):
        with open('config.txt') as f:
            data = f.read()
            f.close()

        settings = json.loads(data)
        self.device = settings["device_id"]
        self.database = Database(self.device)

        self.ref = self.database.get_ref()
        self.ser = uart_utils.initialize_serial()
        self.animationPlayer = AnimationPlayer()
        self.speechArbitrator = SpeechArbitrator(self.animationPlayer)

        #self.imu = IMU.IMU()

        # array of 'state' vectors
        #   [linear accY, speed (GPS) mph, delta speed (GPS) m/s^2]
        self.state = [[0, 0, 0]] 

        self.should_suggest = settings["enable_suggest"]
  

    def change_config(self):
        f = open('config.txt', "w")
        dictionary = {"device_id": self.device, "enable_suggest": self.should_suggest}
        f.write(json.dumps(dictionary))
        f.close()

    def __update_state(self, accY, speed, dt):
        state_length = 100 # how many previous states we keep track of
        mph_to_mps = 0.44704
        delta_speed = (speed - self.state[len(self.state)][1]) * mph_to_mps / dt
        if len(self.state) < state_length:
            self.state.append([accY, speed, delta_speed])
        else:
            self.state = [[accY, speed, delta_speed]] + self.state[0 : state_length - 1]

    def try_uart_read(self):
        # try reading comms from UART
        received_data = uart_receiver.read_all(self.ser)
        # process received string
        if (len(received_data) != 0):       
            raw_data_str = uart_utils.byte2str(received_data)
            data_src, data_str = uart_receiver.extract_msg(raw_data_str)
            print("received: " + data_str + " -from device " + str(data_src))
            return data_str
        return None


    def run(self):
        led_thread = threading.Thread(target=self.animationPlayer.play)
        led_thread.start()
        while(1):
            speech_str = self.try_uart_read()
            if (speech_str != None):
                speech_code = self.speechArbitrator.arbitrate_speech(speech_str)
                if (speech_code == 2):
                    self.should_suggest = True
                    self.animationPlayer.queueAnimation(Animation(3))
                elif (speech_code == 3):
                    self.should_suggest = False
                    self.animationPlayer.queueAnimation(Animation(4))


controller = Main_Control()
controller.run()