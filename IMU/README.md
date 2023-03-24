# IMU
This directory contains all the code relevant to interfacing and filtering data from every sensor on 
the [berryIMU V3](https://ozzmaker.com/berryimu-quick-start-guide/)
## Overview of files
### sensor.py
A base class that establishes the base read, write, and init functionality to the berryIMU sensors

### accelerometer.py
Inherits from `sensor.py` ands and update loop that reads relevant addresses from the sensors and filters the data with median filters,
averaging, IIR filters, and other conventional filtering techniques

### gyro.py
Same as `acceleromter.py` but for the gyroscope on the berryIMU. There is less heavy filtering on this gyroscope

### magnetometer.py
Same as `acceleromter.py` but for the gyroscope on the berryIMU. There is less heavy filtering on this gyroscope

### constants.py
Contains all the relevant filter constants and kalman filter constants for the sensor signal processing

### LIS3MDL.py
Contains the relevant address lookups for the LI3MDL magnetometer on the BerryIMU

### LSM6DSL.py
Contains the relevant address lookups for the LSM6DSL accelerometer/gyroscope on the BerryIMU

### IMU.py
A wrapper object that provides high level functionality and integration of all three positional sensors. Also runs the integrated kalman filter for state estimation
