import json
import sys
import time
import suggest
from dummy import *
from firebase_rt import *
import firebase_admin
from firebase_admin import credentials, storage, db
import threading
import comms.uart_proc as uart_utils
import comms.uart_rec as uart_receiver
import IMU.IMU as IMU

class Main_Control:
    def __init__(self):
        with open('config.txt') as f:
            data = f.read()
            f.close()

        settings = json.loads(data)

        self.should_suggest = settings["enable_suggest"]
        self.device = settings["device_id"]

        self.database = Database(self.device)

        self.ref = self.database.get_ref()
        self.ser = uart_utils.initialize_serial()

        #self.imu = IMU.IMU()

        # array of 'state' vectors
        #   [linear accY, speed (GPS) mph, delta speed (GPS) m/s^2]
        self.state = [[0, 0, 0]] 

        # message sent by Device 1 (TX/RX pins 9/10) and Device 2 (TX/RX pins 7/8)
        self.d1msg = ""
        self.d2msg = ""

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

            # Speech Detection connected to Teensy UART Pins 9/10 (Serial2)
            if (data_src == 1):
                self.d1msg = data_str;
            # Camera (Stop Sign Detection) connected to Teensy UART Pins 7/8
            elif (data_src == 2):
                self.arbitrate_driver_state(data_str)

    def arbitrate_driver_state(self, data_str):
        data_list = data_str.split(',')
        if (len(data_list) != 9):
            return
        if (data_list[5] == "True" or data_list[6] == "True"):
            suggest.driver_tired()
            print("Driver is Tired")
        if (data_list[8] == "True"):
            suggest.driver_distracted()
            print("Driver is distracted")
            #tired
            #asleep
            #looking away
            #distracted
    def run(self):
        while(1):
            self.try_uart_read()




controller = Main_Control()
controller.run()