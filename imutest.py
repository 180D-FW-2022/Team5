import IMU.IMU as IMU

imu = IMU.IMU()

while(True):
    sleep(0.5)
    print(imu.linearAcc())