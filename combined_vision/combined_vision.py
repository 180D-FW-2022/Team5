import sign_tracker
import Driver_state
import threading
import queue
import cv2
import serial
import time

cap = cv2.VideoCapture(0)
sign_cam = None
if cap.get(cv2.CAP_PROP_FOURCC) != 1448695129: # number unique to driver-facing webcam
    sign_cam = cap
    cap = cv2.VideoCapture(1)


q = queue.Queue()



def run_driver_detect(queue_object, camera, use_picam=False):
    ds = Driver_state.DriverState(queue_object, camera)
    ds.runContinuously(True)


def run_stop_signs(queue_object, camera, use_picam=True):
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


sign_thread = threading.Thread(target=run_stop_signs, args=(q, sign_cam, False))
driver_thread = threading.Thread(target=run_driver_detect, args=(q, cap, False))

def initialize_serial():
    ser = serial.Serial ("/dev/ttyS0", 9600, timeout=1)    #Open port with baud rate
    print("===== Serial Receiver Initialized =====")
    print(ser)
    return ser
ser = initialize_serial()

sign_thread.start()
driver_thread.start()

while True:
    time.sleep(0.1)
    if not q.empty():
        
        payload = q.get()
        b = (payload + "\0").encode('utf-8')
        ser.write(b)
        print("payload", payload)
