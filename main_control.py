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

import pvporcupine
from leds.AnimationSender import AnimationSender
from speech.hotkey import PorcupineDemo
from speech.SpeechDetector import SpeechDetector
from speech.StateArbitrator import StateArbitrator
from AudioSuggester import AudioSuggester

import i2cgps as gps
from firebase_rt import Database

import os

print("connecting cams")
# res = os.popen("sudo udevadm info --query=all /dev/video0 | grep 'VENDOR_ID\|MODEL_ID\|SERIAL_SHORT'")
res = os.popen("sudo udevadm info --query=all /dev/video0 | grep 'VENDOR_ID\|MODEL_ID\|SERIAL_SHORT'")
driver_vendor = "0c45"
driver_cam = None
sign_cam = None
if driver_vendor in res:
    driver_cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
    sign_cam = cv2.VideoCapture(2, cv2.CAP_V4L2)
else:
    driver_cam = cv2.VideoCapture(2, cv2.CAP_V4L2) 
    sign_cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

driver_cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 320
height = 240
driver_cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
driver_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
# cap = cv2.VideoCapture(0) 

# if cap.get(cv2.CAP_PROP_FOURCC) != 1448695129: # number unique to driver-facing webcam
#     sign_cam = cap
#     cap = cv2.VideoCapture(2)
# else:
#     sign_cam = cv2.VideoCapture(2)
print("connected cams")


def run_driver_detect(queue_object, camera, use_picam=False, calibration_queue=None):
    ds = Driver_state.DriverState(queue_object, camera, calib=calibration_queue)
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

        settings = json.loads(data)
        self.device = settings["device_id"]

        self.database = Database(self.device)
        self.ref = self.database.get_ref()

        self.audioSuggester = AudioSuggester(settings["enable_suggest"])
        self.animationSender = AnimationSender()
        self.calibration_queue = queue.Queue()
        self.stateArbitrator = StateArbitrator(self.animationSender, self.audioSuggester, self.calibration_queue)
        #self.threadedSpeechDetector = ThreadedSpeechDetector(self.stateArbitrator)
        self.speechDetector = SpeechDetector(self.stateArbitrator)

        self.stateArbitrator.incident_summary = {
            "Speeding": 0,
            "Stop Violation": 0,
            "Tired While Driving": 0,
            "Distracted Driver": 0,
            "High acceleration": 0
        }
        self.incident_summary_lock = threading.Lock()

        # Initialize hot key detector
        with open('./speech/.env') as f:
            ACCESS_KEY = f.readline().strip()
        #PATH = "./speech/Hey-Edward_en_mac_v2_1_0/Hey-Edward_en_mac_v2_1_0.ppn"
        PATH = "./speech/Hey-Edward_en_raspberry-pi_v2_1_0/Hey-Edward_en_raspberry-pi_v2_1_0.ppn"

        # Start the threaded implementation of hot key detection for "Hey Edward"
        # This object also interfaces with self.speechDetector and runs the Google speech
        # API calls
        self.porcupine = PorcupineDemo(
            speech_detector=self.speechDetector,
            access_key=ACCESS_KEY,
            library_path=pvporcupine.LIBRARY_PATH,
            model_path=pvporcupine.MODEL_PATH,
            keyword_paths=[PATH],
            sensitivities=[0.65],
            input_device_index=-1,
            output_path=None).start()
    
        self.stop_sensor = Sensor(5,0.2)
        self.sleep_sensor = Sensor(10,0.3)
        self.speed_sensor = Sensor(10,0.25)
        self.distract_sensor = Sensor(10,0.3)
        self.accel_sensor = Sensor(10, 0.2)
        self.location_sensor = Sensor(600, 15)

        speed_incident = Incident("Speeding", 60, [(self.speed_sensor.find_above, 30)], self.audioSuggester.slow_down)
        stop_incident = Incident("Stop Violation", 30, [(self.stop_sensor.find_case, 1)], self.audioSuggester.blew_stop)
        tired_incident = Incident("Tired While Driving", 30, [(self.sleep_sensor.find_case, 1)], self.audioSuggester.driver_distracted)
        distract_incident = Incident("Distracted Driver", 30, [(self.distract_sensor.find_case, 1)], self.audioSuggester.driver_distracted)
        accel_incident = Incident("High acceleration", 30, [(self.accel_sensor.find_above, 1000)], self.audioSuggester.aggressive)

        self.my_incidents = [speed_incident, stop_incident, tired_incident, distract_incident, accel_incident]
        self.imu = IMU.IMU()

        self.ser = uart_utils.initialize_serial()
        self.gps = gps.GPS()
        self.gps_delay = 0.5
        self.gps_prev_time = time.time() - 0.5



    def init_signs(self):
        self.sign_q = queue.Queue()
        
        sign_thread = threading.Thread(target=run_stop_signs, args=(self.sign_q, sign_cam, False))
        sign_thread.start()


    def init_driver(self):
        self.driver_q = queue.Queue()
        
        driver_thread = threading.Thread(target=run_driver_detect, args=(self.driver_q, driver_cam, False, self.calibration_queue))
        driver_thread.start()

    def init_io(self):
        self.led_thread = threading.Thread(target=self.animationSender.start)
        self.led_thread.start()
        print("LED Thread started")

        self.suggest_thread = threading.Thread(target=self.audioSuggester.run)
        self.suggest_thread.start()
        print("suggest Thread started")

        # bootup complete indicator light
        self.animationSender.queueSend(1)

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
        
        accel_arr = list(self.imu.linearAcc())
        self.accel_sensor.push(accel_arr[1])
        
        
        if time.time() > self.gps_prev_time + self.gps_delay:
            self.gps.readGPS()
            self.gps_prev_time = time.time()
            self.speed_sensor.push(self.gps.speed())
            self.location_sensor.push((self.gps.lat(), self.gps.long()))
            if (self.gps.lat() != 0 and self.gps.long() != 0):
                self.database.uploadGPS(self.gps.lat(), self.gps.long())

            print("lat", self.gps.lat(), "long", self.gps.long(),"speed", self.gps.speed())



        # check for incidents
        for inc in self.my_incidents:
            # if inc.name == "Tired While Driving":
                # print("testing tired")
                # print(self.sleep_sensor.find_case(1), len(self.sleep_sensor.hist))
                # print(self.sleep_sensor.hist)
            if inc.check_incident():
                #report
                print("incident:", inc.name)
                self.incident_summary_lock.acquire()
                self.stateArbitrator.incident_summary[inc.name] += 1
                self.incident_summary_lock.release()

if __name__ == '__main__':
    controller = Controller()
    controller.init_signs()
    controller.init_driver()
    controller.init_io()
    
    while True:
        controller.run_iter()
