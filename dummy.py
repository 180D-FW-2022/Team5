import random

def curr_speed():
    # will replace with actual speed from GPS
    return random.random()*20

def curr_acc(imu):
    # will replace with linear acc from IMU
    return imu.linearAcc()

def stop_sign():
    # checks stop sign size and location to determine if driver should slpw
    return False

def distracted(d2msg):
     # checks if driver is not looking forward
    data = d2msg.split(',')
    asleep = data[6]
    looking_away = [7]
    #distracted = [8]

    return asleep or looking_away 

def stop_blown():
    # checks if driver didn't stop for a stop sign
    return False
