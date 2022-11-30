from IMU.LIS3MDL import *
from constants import *

import sensor
import statistics
import sys

class Magnetometer(sensor.Sensor):
    def __init__(self, medianFilterLength):
        super().__init__(LIS3MDL_ADDRESS, \
            LIS3MDL_OUT_X_L, \
            LIS3MDL_OUT_X_H, \
            LIS3MDL_OUT_Y_L, \
            LIS3MDL_OUT_Y_H, \
            LIS3MDL_OUT_Z_L, \
            LIS3MDL_OUT_Z_H)

        # historical values for median filter
        self.logX = [1 for i in range(0, medianFilterLength)]
        self.logY = [1 for i in range(0, medianFilterLength)]
        self.logZ = [1 for i in range(0, medianFilterLength)]

        # Use calibrateBerryIMU.py to get calibration values
        # Calibrating the compass isnt mandatory, however a calibrated
        # compass will result in a more accurate heading value.
        self.magXmin =  0
        self.magYmin =  0
        self.magZmin =  0
        self.magXmax =  0
        self.magYmax =  0
        self.magZmax =  0

        self.__initialize()

    def update(self):
        MAGx, MAGy, MAGz = self.readRaw()

        #Apply compass calibration
        MAGx -= (self.magXmin + self.magXmax) /2
        MAGy -= (self.magYmin + self.magYmax) /2
        MAGz -= (self.magZmin + self.magZmax) /2

        MAGx_f, MAGy_f, MAGz_f = self.__filter(MAGx, MAGy, MAGz)

        return MAGx_f, MAGy_f, MAGz_f


    def __filter(self, MAGx, MAGy, MAGz):
        ### IIR LPF
        MAGx =  MAGx  * MAG_LPF_FACTOR + self.logX[0]*(1 - MAG_LPF_FACTOR);
        MAGy =  MAGy  * MAG_LPF_FACTOR + self.logY[0]*(1 - MAG_LPF_FACTOR);
        MAGz =  MAGz  * MAG_LPF_FACTOR + self.logZ[0]*(1 - MAG_LPF_FACTOR);

        ### MEDIAN FILTER
        # remove last elements
        self.logX.pop()
        self.logY.pop()
        self.logZ.pop()
        # add updated first element as most recent
        self.logX = [MAGx] + self.logX
        self.logY = [MAGy] + self.logY
        self.logZ = [MAGz] + self.logZ
        # find median of each array
        x = statistics.median(self.logX)
        y = statistics.median(self.logY)
        z = statistics.median(self.logZ)

        return x, y, z

    def __initialize(self):
        ### WHO AM I CHECK
        try:
            LIS3MDL_WHO_AM_I_response = (self.bus.read_byte_data(LIS3MDL_ADDRESS, LIS3MDL_WHO_AM_I))
        except IOError as f:
            print('ERROR: No LIS3MDL was found...')
            sys.exit()
        else:
            if (LIS3MDL_WHO_AM_I_response == 0x3D):
                print("Found LIS3MDL for magnetometer...")

        ### SETUP
        #initialise the magnetometer
        self.writeByte(LIS3MDL_CTRL_REG1, 0b11011100)         # Temp sesnor enabled, High performance, ODR 80 Hz, FAST ODR disabled and Selft test disabled.
        self.writeByte(LIS3MDL_CTRL_REG2, 0b00100000)         # +/- 8 gauss
        self.writeByte(LIS3MDL_CTRL_REG3, 0b00000000)         # Continuous-conversion mode
