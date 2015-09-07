from math import radians, cos, sin, asin, sqrt


class Coordinates():
    def __init__(self, latitude, longitude):
        #todo: add validation
        self.latitude = latitude
        self.longitude = longitude

    @classmethod
    def from_string(cls, s):
        return Coordinates(float(s.split(',')[0]), float(s.split(',')[1]))

    def __str__(self):
        return "{},{}".format(self.latitude, self.longitude)

    def distance(self, other):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """

        for param in [self.longitude, self.latitude, other.longitude, other.latitude]:
            if param is None:
                return float('inf')

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