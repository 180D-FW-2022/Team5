import json
import sys
import time
from suggest import *
from dummy import *
from firebase_rt import *
from ed_speech_2 import SpeechDetect
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
        self.speech = SpeechDetect(self.should_suggest)

        self.ref = self.database.get_ref()
        self.ser = uart_utils.initialize_serial()

        self.imu = IMU.IMU()

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

            # Inward Facing Camera connected to Teensy UART Pins 9/10 (Serial2)
            if (data_src == 1):
                self.d1msg = data_str;
            # Forward Facing Camera (Stop Sign Detection) connectedto Teensy UART Pins 7/8
            elif (data_src == 2):
                self.d2msg = data_str;

    def run(self):
        t1 = threading.Thread(target=self.speech.detect_speech, daemon=True)
        t1.start()
        t0 = time.time()
        while(1):
            # check if we should provide audio suggestions
            should = self.speech.suggestSetting()

            # update config if settings changed
            if should != self.should_suggest:
                self.should_suggest = should
                if should:
                    enable_suggestions()
                else:
                    disable_suggestions()
                self.change_config()

            self.try_uart_read()
            
            # get current speed
            speed = curr_speed()
            acc = curr_acc(self.imu)
            speedWarn = speed > 65
            dt = time.time() - t0
            t0 = time.time()
            self.__update_state(acc[1], speed, dt)
            
            if speedWarn:
                self.database.uploadData(speed, acc, "speed")
                if self.should_suggest:
                    warn_speed(65, round(speed,2))
            if self.speech.shouldReport():
                say_phrase("Your current acceleration is " + str(round(acc[0], 2)))
                self.speech.reportDone()
            # check stop sign
            if self.should_suggest and stop_sign():
                approach_stop()

            # check gaze
            # if distracted(self.d2msg):
            #     self.database.uploadData(speed, acc, "distracted")
            #     if self.should_suggest:
            #         driver_distracted()

            # check stop blown
            if stop_sign() and not is_slowing_down():
                self.database.uploadData(speed, acc, "stopBlown")
                if self.should_suggest:
                    blew_stop()

            if self.speech.shouldPowerOff():
                power_off()
                sys.exit()




controller = Main_Control()
controller.run()
