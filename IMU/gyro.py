from IMU.LSM6DSL import *

import IMU.sensor as sensor
import sys

class Gyroscope(sensor.Sensor):
    def __init__(self):
        super().__init__(LSM6DSL_ADDRESS,\
            LSM6DSL_OUTX_L_G, \
            LSM6DSL_OUTX_H_G, \
            LSM6DSL_OUTY_L_G, \
            LSM6DSL_OUTY_H_G, \
            LSM6DSL_OUTZ_L_G, \
            LSM6DSL_OUTZ_H_G)

        # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
        self.G_GAIN = 0.070

        self.__initialize()

    def update(self):
        GYRx, GYRy, GYRz = self.readRaw()

        #Convert Gyro raw to degrees per second
        rate_gyr_x =  GYRx * self.G_GAIN
        rate_gyr_y =  GYRy * self.G_GAIN
        rate_gyr_z =  GYRz * self.G_GAIN

        return rate_gyr_x, rate_gyr_y, rate_gyr_z

    def __filter(self, GYRx, GYRy, GYRz):
        return GYRx, GYRy, GYRz

    def __initialize(self):
        ### WHO AM I CHECK
        try:
            LSM6DSL_WHO_AM_I_response = (self.bus.read_byte_data(LSM6DSL_ADDRESS, LSM6DSL_WHO_AM_I))
        except IOError as f:
            print('ERROR: No LSM6DSL was found...')
            sys.exit()
        else:
            if (LSM6DSL_WHO_AM_I_response == 0x6A):
                print("Found LSM6DSL for gyroscope...")

        ### SETUP
        #initialise the gyroscope
        self.writeByte(LSM6DSL_CTRL2_G,0b10011100)            #ODR 3.3 kHz, 2000 dps
