import cv2
import dlib
import numpy as np
import time
import serial

from Utils import get_face_area
from Eye_Dector_Module import EyeDetector as EyeDet
from Pose_Estimation_Module import HeadPoseEstimator as HeadPoseEst
from Attention_Scorer_Module import AttentionScorer as AttScorer
from constants import *

class DriverState:
    def __init__(self, queue, cap=None):
        # serial port object for uart. Replace with -1 if not using
        self.queue = queue

        self.ctime = 0  # current time (used to compute FPS)
        self.ptime = 0  # past time (used to compute FPS)
        self.prev_time = 0  # previous time variable, used to set the FPS limit
        self.fps_lim = 3  # FPS upper limit value, needed for estimating the time for each frame and increasing performances
        self.time_lim = 1. / self.fps_lim  # time window for each frame taken by the webcam

        # instantiation of the dlib face detector object
        self.Detector = dlib.get_frontal_face_detector()
        # instantiation of the dlib keypoint detector model
        self.Predictor = dlib.shape_predictor("./combined_vision/shape_predictor_68_face_landmarks.dat")

        # instantiation of the eye detector and pose estimator objects
        self.Eye_det = EyeDet(show_processing=False)

        self.Head_pose = HeadPoseEst(show_axis=True)

        # instantiation of the attention scorer object, with the various thresholds
        self.Scorer = AttScorer(self.fps_lim,
            ear_tresh=0.2, \
            ear_time_tresh=2, \
            gaze_tresh=0.2, \
            gaze_time_tresh=2, \
            pitch_tresh=35, \
            yaw_tresh=28, \
            pose_time_tresh=2.5, \
            verbose=False)

        if cap:
            cv2.setUseOptimized(True)
            self.cap = cap
        else:
            self.cap = self.__initOpenCV()





    def __initOpenCV(self):
        cv2.setUseOptimized(True)
        cap = cv2.VideoCapture(CAPTURE_SOURCE)
        if not cap.isOpened():
            print("ERROR: Cannot open camera. Exiting...")
            exit(1)

        return cap

    '''
     Examines a single frame from the selected camera and extracts:
     - gaze score
     - percetage of time eyes closed vs. open (perclos)
     - Eye aspect Ratio (EAR)
     - Euler angles of the head posture (roll, pitch, yaw)
     As well as high level metrics:
     - is driver tired
     - is driver asleep
     - is driver looking away
     - is driver distracted
     With the option to print out all metrics to the console verbosely
     in a formatted string
    '''
    def update(self, verbose=False):
        ret, frame = self.cap.read()
        if not ret:
            print("ERROR: Can't receive frame from camera/stream end. Exiting...")
            exit(1)

        # if the frame comes from webcam, flip it so it looks like a mirror.
        if CAPTURE_SOURCE == 0:
            frame = cv2.flip(frame, 2)

        # transform the BGR frame in grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # apply a bilateral filter to lower noise but keep frame details
        gray = cv2.bilateralFilter(gray, 5, 10, 10)

        # find the faces using the dlib face detector
        faces = self.Detector(gray)

        if len(faces) > 0:  # process the frame only if at least a face is found

                # take only the bounding box of the biggest face
                faces = sorted(faces, key=get_face_area, reverse=True)
                driver_face = faces[0]

                # predict the 68 facial keypoints position
                landmarks = self.Predictor(gray, driver_face)

                # compute the EAR score of the eyes
                ear = self.Eye_det.get_EAR(frame=gray, landmarks=landmarks)

                # compute the PERCLOS score and state of tiredness
                tired, perclos_score = self.Scorer.get_PERCLOS(ear)

                # compute the Gaze Score
                gaze = self.Eye_det.get_Gaze_Score(
                    frame=gray, landmarks=landmarks)

                # compute the head pose
                _, roll, pitch, yaw = self.Head_pose.get_pose(
                    frame=frame, landmarks=landmarks)

                # evaluate the scores for EAR, GAZE and HEAD POSE
                asleep, looking_away, distracted = self.Scorer.eval_scores(
                    ear, gaze, roll, pitch, yaw)

                if verbose:
                    self.__prettyPrint(perclos_score, ear, roll, pitch, yaw, tired, asleep, looking_away, distracted)

                perclos_score = round(perclos_score, 2)
                ear = round(ear, 2)
                roll = round(roll, 2)
                pitch = round(pitch, 2)
                yaw = round(yaw, 2)

                return perclos_score, ear, roll, pitch, yaw, tired, asleep, looking_away, distracted

        return -1, -1, -1, -1, -1, False, False, False, False

    def __prettyPrint(self, perclos_score, ear, roll, pitch, yaw, tired, asleep, looking_away, distracted):
        print(f'UPDATE LOG: \n\
            EAR: {ear}, \n\
            PERCLOS: {perclos_score}, \n\
            ROLL: {roll}, \n\
            PITCH: {pitch}, \n\
            YAW: {yaw}, \n\
            TIRED: {tired}, \n\
            ASPEEP: {asleep}, \n\
            LOOKING_AWAY: {looking_away}, \n\
            DISTRACTED: {distracted}\n')

    # Runs the update function continously, capped with a max framerate
    # and optionally transmittes the results to the controller
    def runContinuously(self, tx=False):
        while True:
            time.sleep(0.33)
            delta_time = time.perf_counter() - self.prev_time

            # looping too fast
            if delta_time < self.time_lim:
                continue

            # compute the actual frame rate per second (FPS) of the webcam video capture stream
            self.prev_time = time.perf_counter()
            self.ctime = time.perf_counter()
            fps = 1.0 / float(self.ctime - self.ptime)
            self.ptime = self.ctime

            try:
                perclos_score, ear, roll, pitch, yaw, tired, asleep, looking_away, distracted = self.update(verbose=False)
                if tx and ear != -1:
                    payload = f'{ear},{perclos_score},{roll},{pitch},{yaw},{tired},{asleep},{looking_away},{distracted}'
                    payload = f'{1 if tired else 0}{1 if asleep else 0}{1 if looking_away else 0}{1 if distracted else 0}'
                    # print(payload)
                    # self.__txToController(payload)
                    self.queue.put(payload)
            except:
                pass

            

    # Send the data via teensy UART buffer to RX controller Rpi
    def __txToController(self, payload):
        # WARNING: imports are weird so hard-coding this serial transmit
        b = payload.encode('utf-8')
        ser.write(b)
        #uart_send.write_str(self.ser, payload)

if __name__ == "__main__":
    ds = DriverState(-1)
    ds.runContinuously()
