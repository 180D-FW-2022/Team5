
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
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

def gpsDistance(lon1, lat1, lon2, lat2):
    mi = haversine(lon1, lat1, lon2, lat2)

    return mi


# Takes in 2 GPS points in the following format: [lat (deg), long (deg), time (s)]
def gpsSpeed(lon1, lat1, t1, lon2, lat2, t2):
    dx = gpsDistance(lon1, lat1, lon2, lat2) # in miles
    dt = (t2 - t1) / 3600.00 # in hours

    return (dx/dt)


def main():
    lat1 = 34.069705 
    lon1 = -118.455109
    lat2 = 36.218040
    lon2 = -115.137930
    
    d = gpsDistance(lon1, lat1, lon2, lat2)
    print("Distance: " + str(d))

    t1 = 0
    t2 = 3600 * 5
    v = gpsSpeed(lon1, lat1, t1, lon2, lat2, t2)
    print("speed: " + str(v))

if __name__ == "__main__":
    main()
