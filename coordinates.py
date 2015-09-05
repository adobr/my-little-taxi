from math import radians, cos, sin, asin, sqrt

class Coordinates():
    def __init__(self, s):
        #todo: add validation
        self.latitude = float(s.split(',')[0])
        self.longitude = float(s.split(',')[1])

    def __str__(self):
        return "{},{}".format(self.latitude, self.longitude)


    def distance(self, other):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians,
                                     [self.longitude, self.latitude, other.longitude, other.latitude])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r