import threading, queue, json, cv2, serial, time
import numpy as np
from firebase_admin import credentials, storage, db

from sensor_class import Sensor
from incident import Incident

import IMU.IMU as IMU
import combined_vision.sign_tracker as sign_tracker
import combined_vision.Driver_state as Driver_state
import comms.uart_proc as uart_utils
import comms.uart_rec as uart_receiver

from leds.AnimationPlayer import AnimationPlayer
from leds.Animation import Animation
from speech.ThreadedSpeechDetector import ThreadedSpeechDetector
from speech.StateArbitrator import StateArbitrator
from AudioSuggester import AudioSuggester

import gps
from firebase_rt import Database

import os

print("connecting cams")
# res = os.popen("sudo udevadm info --query=all /dev/video0 | grep 'VENDOR_ID\|MODEL_ID\|SERIAL_SHORT'")
res = os.popen("sudo udevadm info --query=all /dev/video0 | grep 'VENDOR_ID\|MODEL_ID\|SERIAL_SHORT'")
driver_vendor = "0c45"
driver_cam = None
sign_cam = None
if driver_vendor in res:
    driver_cam = cv2.VideoCapture(0) 
    sign_cam = cv2.VideoCapture(2)
else:
    driver_cam = cv2.VideoCapture(2) 
    sign_cam = cv2.VideoCapture(0)
    
# cap = cv2.VideoCapture(0) 

# if cap.get(cv2.CAP_PROP_FOURCC) != 1448695129: # number unique to driver-facing webcam
#     sign_cam = cap
#     cap = cv2.VideoCapture(2)
# else:
#     sign_cam = cv2.VideoCapture(2)
print("connected cams")


def run_driver_detect(queue_object, camera, use_picam=False):
    ds = Driver_state.DriverState(queue_object, camera)
    ds.runContinuously(True)


def run_stop_signs(queue_object, camera, use_picam=False):
    det = sign_tracker.my_detector([224,224])
    while True:
        frame = None
        if use_picam:
            frame = camera.capture_array()[:,:,:3]
        else:
            _, frame = camera.read()
        r = det.my_detect(frame, 0.3)
        if r:
            # print(r)
            queue_object.put(r)


class Controller:
    def __init__(self) -> None:
        with open('config.txt') as f:
            data = f.read()
            f.close()

        settings = json.loads(data)
        self.device = settings["device_id"]

        self.database = Database(self.device)
        self.ref = self.database.get_ref()

        self.audioSuggester = AudioSuggester()
        self.animationPlayer = AnimationPlayer()
        self.stateArbitrator = StateArbitrator(self.animationPlayer, self.audioSuggester, settings["enable_suggest"])
        self.threadedSpeechDetector = ThreadedSpeechDetector(self.stateArbitrator)
    
        self.stop_sensor = Sensor(5,0.2)
        self.sleep_sensor = Sensor(10,0.3)
        self.speed_sensor = Sensor(10,0.25)
        self.distract_sensor = Sensor(10,0.3)
        self.accel_sensor = Sensor(10, 0.2)
        self.location_sensor = Sensor(600, 15)

        speed_incident = Incident("Speeding", 60, [(self.speed_sensor.find_above, 70)])
        stop_incident = Incident("Stop Violation", 30, [(self.stop_sensor.find_case, 1), (self.speed_sensor.not_find_below, 5)])
        tired_incident = Incident("Tired While Driving", 30, [(self.sleep_sensor.find_case, 1)])
        distract_incident = Incident("Distracted Driver", 30, [(self.distract_sensor.find_case, 1)])
        accel_incident = Incident("High acceleration", 30, [(self.accel_sensor.find_above, 1000)])

        self.my_incidents = [speed_incident, stop_incident, tired_incident, distract_incident, accel_incident]
        self.imu = IMU.IMU()

        self.ser = uart_utils.initialize_serial()
        self.gps = gps.GPS()



    def init_signs(self):
        self.sign_q = queue.Queue()
        
        sign_thread = threading.Thread(target=run_stop_signs, args=(self.sign_q, sign_cam, False))
        sign_thread.start()


    def init_driver(self):
        self.driver_q = queue.Queue()
        driver_thread = threading.Thread(target=run_driver_detect, args=(self.driver_q, driver_cam, False))
        driver_thread.start()

    def try_uart_read(self):
        # try reading comms from UART
        received_data = uart_receiver.read_all(self.ser)
        # process received string
        if (len(received_data) != 0):       
            raw_data_str = uart_utils.byte2str(received_data)
            # data_src, data_str = uart_receiver.extract_msg(raw_data_str)
            data_str = raw_data_str
            data_src = 1
            print("received: " + data_str + " -from device " + str(data_src))

            # Speech Detection connected to Teensy UART Pins 9/10 (Serial2)
            if (data_src == 1):
                self.sa.arbitrate_speech(data_str)
                if (data_str == "4"):
                    self.audioSuggester.enable_suggestions()
                if (data_str == "3"):
                    self.audioSuggester.disable_suggestions()
            # Camera (Stop Sign Detection) connected to Teensy UART Pins 7/8

    def init_io(self):
        self.led_thread = threading.Thread(target=self.animationPlayer.play)
        self.led_thread.start()
        print("LED Thread started")

        self.suggest_thread = threading.Thread(target=self.audioSuggester.run)
        self.suggest_thread.start()
        print("suggest Thread started")

        self.threadedSpeechDetector.run()
        print("speech processing Thread started")

    def run_iter(self):
        self.stateArbitrator.loop_state_updater()
        # speech things
        # self.try_uart_read()

        # update sensors
        while not self.sign_q.empty():
            print("sign")
            self.sign_q.get()
            self.stop_sensor.push(1)
        
        while not self.driver_q.empty():
            
            result = self.driver_q.get()
            print(result)
            if '1' in result[0:2]:
                self.sleep_sensor.push(1)
            if '1' in result[2:]:
                self.distract_sensor.push(1)
        
        accel_arr = self.imu.linearAcc()
        self.accel_sensor.push(np.linalg.norm(accel_arr[:2]))
        
        #self.gps.readGPS()
        self.speed_sensor.push(self.gps.speed())
        self.location_sensor.push((self.gps.lat(), self.gps.long()))


        # check for incidents
        for inc in self.my_incidents:
            if inc.check_incident():
                #report
                print("incident:", inc.name)

if __name__ == '__main__':
    controller = Controller()
    controller.init_signs()
    controller.init_driver()
    controller.init_io()
    
    while True:
        controller.run_iter()