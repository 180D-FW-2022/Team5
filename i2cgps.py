#! /usr/bin/python
import time
import smbus
import signal
import sys
from math import *

gpsReadInterval = 0.03

class Message:
    def __init__(self, lon, lat, sat, qual) -> None:
        self.longitude = lon
        self.latitude = lat
        self.num_sats = sat
        self.gps_qual = qual
        pass

class GPS:

    

    def handle_ctrl_c(self, signal, frame):
        sys.exit(130)

    def __init__(self) -> None:
        # This will capture exit when using Ctrl-C
        self.BUS = None
        self.connectBus()
        self.address = 0x42
        self.prev_state = [0, 0, 0, 0, 0]
        self.state = [0, 0, 0, 0, 0]
        
        signal.signal(signal.SIGINT, self.handle_ctrl_c)


    def connectBus(self):
        self.BUS = smbus.SMBus(1)


    def parseResponse(self, gpsLine):
        if (gpsLine.count(36) == 1):                           # Check #1, make sure '$' doesnt appear twice
            # Check #2, 83 is maximun NMEA sentenace length.
            if len(gpsLine) < 84:
                CharError = 0
                # Check #3, Make sure that only readiable ASCII charaters and Carriage Return are seen.
                for c in gpsLine:
                    if (c < 32 or c > 122) and c != 13:
                        CharError += 1
                if (CharError == 0):  # Only proceed if there are no errors.
                    gpsChars = ''.join(chr(c) for c in gpsLine)
                    if (gpsChars.find('txbuf') == -1):          # Check #4, skip txbuff allocation error
                        # Check #5 only split twice to avoid unpack error
                        gpsStr, chkSum = gpsChars.split('*', 2)
                        gpsComponents = gpsStr.split(',')
                        chkVal = 0
                        # Remove the $ and do a manual checksum on the rest of the NMEA sentence
                        for ch in gpsStr[1:]:
                            chkVal ^= ord(ch)
                        # Compare the calculated checksum with the one in the NMEA sentence
                        if (chkVal == int(chkSum, 16)):
                            print(gpsChars)
                            if "GNGLL" in gpsChars:
                                sections = gpsChars.split(',')
                                self.msg = Message(float(sections[3]) if sections[3] else 0, float(sections[1]) if sections[1] else 0, 0, 0)
                                return True
                            else:
                                return False
                            # msg.latitude = float(sections[1]) if sections[1] else 0
                            # msg.longitude = float(sections[3]) if sections[3] else 0
                            # msg.num_sats = 0
                            # msg.gps_qual




    def readGPS(self):
        c = None
        response = []
        try:
            t_read = time.time()
            while True:  # Newline, or bad char.
                c = self.BUS.read_byte(self.address)
                if c == 255:
                    return False
                elif c == 10:
                    break
                else:
                    response.append(c)
            if self.parseResponse(response):
                self.updateState(self.msg, t_read)
        except IOError:
            self.connectBus()
        except Exception:
            exit("exception, exiting")

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
        return self.gpsSpeed(long1, lat1, t1, long2, lat2, t2)

    # Returns haversine distance between 2 lat and long coordinates in miles
    def gpsDistance(self, lon1, lat1, lon2, lat2):
        mi = self.haversine(lon1, lat1, lon2, lat2)

        return mi

    # Takes in 2 GPS points in the following format: [lat (deg), long (deg), time (s)]
    def gpsSpeed(self, lon1, lat1, t1, lon2, lat2, t2):
        dx = self.gpsDistance(lon1, lat1, lon2, lat2) # in miles
        dt = (t2 - t1 + 0.01) / 3600.00 # in hours
        print("time", dt, "dist", dx)

        return (dx/dt)


    def haversine(self, lon1, lat1, lon2, lat2):
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

    def updateState(self, msg, t_read):
        self.prev_state = self.state
        self.state = [msg.longitude, msg.latitude, t_read, \
                int(msg.num_sats), int(msg.gps_qual)]

if __name__ == "__main__":
    gps = GPS()
    while True: 
        time.sleep(gpsReadInterval)
        gps.readGPS()
        print(gps.lat())
        print(gps.long())
        print(gps.speed())
        print()
