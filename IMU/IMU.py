import accelerometer
import gyro
import magnetometer
import datetime
import math

from constants import *


class IMU:
    def __init__(self):
        self.acc = accelerometer.Accelerometer(ACC_MEDIANTABLESIZE)
        self.gyro = gyro.Gyroscope()
        self.mag = magnetometer.Magnetometer(MAG_MEDIANTABLESIZE)

        self.refTime = datetime.datetime.now()

        self.y_bias = 0.0
        self.x_bias = 0.0
        self.XP_00 = 0.0
        self.XP_01 = 0.0
        self.XP_10 = 0.0
        self.XP_11 = 0.0
        self.YP_00 = 0.0
        self.YP_01 = 0.0
        self.YP_10 = 0.0
        self.YP_11 = 0.0

    def linearAcc(self):
        return self.acc.update()

    def gyroIntegration(self):
        b = datetime.datetime.now() - self.refTime
        LP = b.microseconds/(1000000*1.0)
        rate_gyr_x, rate_gyr_y, rate_gyr_z = self.gyro.update()

        #Calculate the angles from the gyro.
        gyroXangle+=rate_gyr_x*LP
        gyroYangle+=rate_gyr_y*LP
        gyroZangle+=rate_gyr_z*LP

        return gyroXangle, gyroYangle, gyroZangle

    def tiltCompensatedHeading(self):
        ACCx, ACCy, ACCz = self.acc.update()
        MAGx, MAGy, MAGz = self.mag.update()

        #Calculate heading
        heading = 180 * math.atan2(MAGy,MAGx)/M_PI

        #Only have our heading between 0 and 360
        if heading < 0:
            heading += 360

        #Normalize accelerometer raw values.
        accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
        accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


        #Calculate pitch and roll
        pitch = math.asin(accXnorm)
        roll = -math.asin(accYnorm/math.cos(pitch))

        #X compensation
        magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)

        #Y compensation
        magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch

        #Calculate tilt compensated heading
        tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

        if tiltCompensatedHeading < 0:
            tiltCompensatedHeading += 360

        return tiltCompensatedHeading

    def kalmanStateEstimate(self):
        b = datetime.datetime.now() - self.refTime
        LP = b.microseconds/(1000000*1.0)
        print("LOOP TIME: " + str(LP))

        rate_gyr_x, rate_gyr_y, rate_gyr_z = self.gyro.update()

        ACCx, ACCy, ACCz = self.acc.update()

        #Convert Accelerometer values to degrees (radial acceleration)
        AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
        AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

        #Change the rotation value of the accelerometer to -/+ 180 and
        #move the Y axis '0' point to up.  This makes it easier to read.
        if AccYangle > 90:
            AccYangle -= 270.0
        else:
            AccYangle += 90.0

        #Kalman filter used to combine the accelerometer and gyro values.
        kalmanY, self.YP_00, self.YP_01, self.YP_10, self.YP_11, self.y_bias = __kalman(AccYangle, rate_gyr_y, LP, self.YP_00, self.YP_01, self.YP_10, self.YP_11, self.y_bias)
        kalmanX, self.XP_00, self.XP_01, self.XP_10, self.XP_11, self.x_bias = __kalman(AccXangle, rate_gyr_x, LP, self.XP_00, self.XP_01, self.XP_10, self.XP_11, self.x_bias)

        return kalmanX, kalmanY



    # Takes in the current state estimate along with the relevant constants
    # and returns the new state estimate
    def __kalman(self, accAngle, gyroRate, DT, P_00, P_01, P_10, P_11, bias):
        x=0.0
        S=0.0

        KFangley = KFangley + DT * (gyroRate - bias)

        P_00 = P_00 + ( - DT * (P_10 + P_01) + Q_angle * DT )
        P_01 = P_01 + ( - DT * P_11 )
        P_10 = P_10 + ( - DT * P_11 )
        P_11 = P_11 + ( + Q_gyro * DT )

        x = accAngle - KFangle
        S = P_00 + R_angle
        K_0 = P_00 / S
        K_1 = P_10 / S

        KFangleX = KFangle + ( K_0 * x )
        bias = bias + ( K_1 * x )

        P_00 = P_00 - ( K_0 * P_00 )
        P_01 = P_01 - ( K_0 * P_01 )
        P_10 = P_10 - ( K_1 * P_00 )
        P_11 = P_11 - ( K_1 * P_01 )

        return KFangle, P_00, P_01, P_10, P_11, bias
