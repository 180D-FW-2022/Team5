import random

def curr_speed():
    # will replace with actual speed from GPS
    return random.random()*20

def curr_acc():
    # will replace with linear acc from IMU
    return random.random()*5

def stop_sign():
    # checks stop sign size and location to determine if driver should slpw
    return False

def distracted():
    # checks if driver is not looking forward
    return False

def stop_blown():
    # checks if driver didn't stop for a stop sign
    return False