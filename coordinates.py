from math import radians, cos, sin, asin, sqrt


class Coordinates():
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    @classmethod
    def from_string(cls, s):
        format_error = "Incorrect ll format: should be two comma separated numbers(e.g. 55.45,37.36)"
        splitted = s.split(',')
        if len(splitted) != 2:
            raise Exception(format_error)
        try:
            latitude = float(splitted[0])
            longitude = float(splitted[1])
        except:
            raise Exception(format_error)
        if latitude > 90.0 or latitude < -90.0:
            raise Exception("Latitude can be in range [-90.0, 90.0]")
        if longitude > 180.0 or longitude < -180.0:
            raise Exception("Longittude can be in range [-180.0, 180.0]")
        print 'Ok, ok {},{}'.format(latitude, longitude)
        return Coordinates(latitude, longitude)

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