import random

def curr_speed():
    # will replace with actual speed from GPS
    return random.random()*20

def curr_acc(imu):
    # will replace with linear acc from IMU
    return imu.linearAcc()

def stop_sign():
    # checks stop sign size and location to determine if driver should slow
    return False


def distracted(d2msg):
     # checks if driver is not looking forward
    data = d2msg.split(',')
    asleep = data[6]
    looking_away = [7]
    #distracted = [8]

    return asleep or looking_away 

#@parameters:
#   states: a vector of previous states found in `main_control.py`
def is_slowing_down(states):
    # checks if driver is actively slowing down given there exists a stop
    # sign they should be slowing down for (as is determined by `stop_sign()`)

    acc_threshold = -10 # min decceleration to deduce "slowing down"
    dv_threshold = -0.9 # m/s^2 deceleration
    speed_threshold = 15 # min speed to pass a stop sign
    count = 0.0 # number of occurences of a "slowing down" state
    percent_slow_down = 0.5 # at least this % of states slowing down to conclude slowing

    for s in states:
        acc = s[0]
        speed = s[1]
        dv = s[2]
        # if slowing down OR speed is less than 15 mph
        if acc < acc_threshold or speed < speed_threshold or dv < dv_threshold:
            count += 1

    return (count / len(states)) >= percent_slow_down
