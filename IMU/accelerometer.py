from IMU.LSM6DSL import *
from constants import *

import sensor
import statistics
import sys

class Accelerometer(sensor.Sensor):
    def __init__(self, medianFilterLength):
        super().__init__(LSM6DSL_ADDRESS,\
            LSM6DSL_OUTX_L_XL, \
            LSM6DSL_OUTX_H_XL, \
            LSM6DSL_OUTY_L_XL, \
            LSM6DSL_OUTY_H_XL, \
            LSM6DSL_OUTZ_L_XL, \
            LSM6DSL_OUTZ_H_XL)

        # historical values for median filter
        self.logX = [1 for i in range(0, medianFilterLength)]
        self.logY = [1 for i in range(0, medianFilterLength)]
        self.logZ = [1 for i in range(0, medianFilterLength)]

        self.__initialize()

    def update(self):
        ACCx, ACCy, ACCz = self.readRaw()
        ACCx_f, ACCy_f, ACCz_f = self.__filter(ACCx, ACCy, ACCz)

        return ACCx_f, ACCy_f, ACCz_f
        #return ACCx, ACCy, ACCz

    def __filter(self, ACCx, ACCy, ACCz):
        ### IIR LPF
        ACCx =  ACCx  * ACC_LPF_FACTOR + self.logX[0]*(1 - ACC_LPF_FACTOR);
        ACCy =  ACCy  * ACC_LPF_FACTOR + self.logY[0]*(1 - ACC_LPF_FACTOR);
        ACCz =  ACCz  * ACC_LPF_FACTOR + self.logZ[0]*(1 - ACC_LPF_FACTOR);

        ### MEDIAN FILTER
        # remove last elements
        self.logX.pop()
        self.logY.pop()
        self.logZ.pop()
        # add updated first element as most recent
        self.logX = [ACCx] + self.logX
        self.logY = [ACCy] + self.logY
        self.logZ = [ACCz] + self.logZ
        # find median of each array
        x = statistics.median(self.logX)
        y = statistics.median(self.logY)
        z = statistics.median(self.logZ)

        return x, y, z

    def __initialize(self):
        ### WHO AM I CHECK
        try:
            LSM6DSL_WHO_AM_I_response = (self.bus.read_byte_data(LSM6DSL_ADDRESS, LSM6DSL_WHO_AM_I))
        except IOError as f:
            print('ERROR: No LSM6DSL was found...')
            sys.exit()
        else:
            if (LSM6DSL_WHO_AM_I_response == 0x6A):
                print("Found LSM6DSL for accelerometer...")

        ### SETUP
        #initialise the accelerometer
        self.writeByte(LSM6DSL_CTRL1_XL,0b10010011)           #ODR 3.33 kHz, +/- 2g , BW = 400hz
        self.writeByte(LSM6DSL_CTRL8_XL,0b11001000)           #Low pass filter enabled, BW9, composite filter
        self.writeByte(LSM6DSL_CTRL3_C,0b01000100)            #Enable Block Data update, increment during multi byte read
