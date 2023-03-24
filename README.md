# README
Welcome to Driver's Edd!
## Overview of files and sub-directories
### main_control.py
This is the main control loop script that is run on the Rpi 4. It handles initialization during which all systems are interfaced with, 
calibrated, and their threads begun, as well as running the 'incident' architecture and dispatching relevant protocols when incidents occur
like uploading data to firebase and starting speaker tasks

### sensor_class.py
This file contains the generalized 'Sensor' class definition which is used in the 'incident' architecture mention above. It is a general data processing 
class that can take data from the IMU, GPS, and other sensors and answer questions like if there are sensor values above or below a set point, which 
is used to modularly piece together incidents in the Incident class

### incident.py
Contains the class definition for the aforementioned Incident class which modularly combines sensor metrics to detect relevant incidents

### led_control.py
Runs the thread that sends LED commands to the Rpi zero via TCP

### i2cgps.py
Interfaces with the GPS, reads data from it via I2C, parses the and runs the NEMA GPS strings, and does the distance and speech calculationos

### firebase_rt.py
Is interfaced with in `main_control.py` and handles all of the data link and upload with our backend server hosted by Firebase

### AudioSuggester.py
Runs the threaded loop that will verbalize text through our speaker. It is used when incidents occur or after voice commands are issued to give feedback to the user

### config.txt
Stores the local state variables of the system that need to persist through power cycling. The two relevant parameters stored are `device_id` and `enable_suggestions`

### comms/
TCP comms software with Rpi zero

### tests/
Unit tests and random debug tests

### combined_vision/
The integrated computer vision pipeline that runs our stop sign forward facing model and the driver facing distractedness model

### speech/
Code for the speech processing pipeline. All the way from using [pvporcupine](https://picovoice.ai/docs/api/porcupine-python/) for hot word detection 
to [speech_processing](https://pypi.org/project/SpeechRecognition/) for speech to text for command processing

### leds/
Contains all the code that runs on the Rpi zero to interface with the NeoPixel and run the speech animations

### driver_state_detection/
Houses legacy code that purely runs the driver state detection model. This was used and kept for debugging and testing. Based on [this](https://github.com/e-candeloro/Driver-State-Detection) project

### IMU/
Module that contains the code we wrote for reading and filtering data from the accelerometer, gyroscope, and other IMU sensors

### stop_signs/
Same as `driver_state_detection/` but for our stop sign models

### edd-app/
Contains all the website code

## Deploying the website
From the website branch, make sure all changes are commited, and then run `npm run deploy` and wait about 5 mins for github pages to update the website. Website is 
available [here](https://180d-fw-2022.github.io/Team5/)
