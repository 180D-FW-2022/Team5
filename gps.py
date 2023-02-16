#! /usr/bin/python
import time
import smbus
import signal
import sys
from math import radians, cos, sin, asin, sqrt

import pynmea2

BUS = None
address = 0x42

class GPS:
    def __init__(self):
        self.BUS = self.__connectBus()
        self.msg = -1

        # State: 
            # [longitude (decimal), latitude (decimal), time stamp of read, 
            # number satelites (int), gps_qual (1 for good, 0 for 
            # "not available")]
        self.prev_state = [0, 0, 0, 0, 0]
        self.state = [0, 0, 0, 0, 0]


    def readGPS(self):
        c = None
        response = []
        try:
            t_read = time.time()
            while True: # Newline, or bad char.
                c = BUS.read_byte(address)
                if c == 255:
                    return False
                elif c == 10:
                    break
                else:
                    response.append(c)

            # convert back to string
            response = ''.join(chr(e) for e in response)
            self.msg = pynmea2.parse(response)
            self.__updateState(self.msg, t_read)
        except IOError:
            self.__connectBus()
        except Exception:
            exit("ERROR: exception in GPS code, exiting...")

    # Returns most recently read longitude position in decimal format
    def long(self):
        return self.state[0]

    # Returns most recently read lattitude position in decimal format
    def lat(self):
        return self.state[1]

    # Returns calculated speed estimate from speed change in lat and long and dt
    # units: mph
    def speed(self):
        long1 = self.prev_state[0]
        lat1 = self.prev_state[1]
        t1 = self.prev_state[2]

        long2 = self.state[0]
        lat2 = self.state[1]
        t2 = self.state[2]
        
        # calc speed with dt
        return self.__gpsSpeed(long1, lat1, t1, long2, lat2, t2)

    # Returns haversine distance between 2 lat and long coordinates in miles
    def __gpsDistance(self, lon1, lat1, lon2, lat2):
        mi = self.__haversine(lon1, lat1, lon2, lat2)

        return mi

    # Takes in 2 GPS points in the following format: [lat (deg), long (deg), time (s)]
    def __gpsSpeed(self, lon1, lat1, t1, lon2, lat2, t2):
        dx = self.__gpsDistance(lon1, lat1, lon2, lat2) # in miles
        dt = (t2 - t1) / 3600.00 # in hours

        return (dx/dt)


    def __haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 3956 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r

    def __connectBus(self):
        BUS = smbus.SMBus(1)
        return BUS

    def __updateState(self, msg, t_read):
        self.prev_state = self.state
        self.state = [msg.longitude, msg.latitude, t_read, \
                int(msg.num_sats), int(msg.gps_qual)]

def main():
    connectBus()
    while True:
        readGPS()

if __name__ == "__main__":
    main()