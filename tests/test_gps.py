import unittest

import sys
sys.path.append('../')

import gps

class TestGPSClass(unittest.TestCase):

    def test_speedFromLatLong(self):
        g = gps.GPS()
        lat1 = 34.069319
        long1 = -118.455977
        lat2 = 34.079008
        long2 = -118.438333

        print(g.gpsDistance(long1, lat1, long2, lat2))
        


if __name__ == "__main__":
    unittest.main()
