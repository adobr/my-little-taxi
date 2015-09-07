import datetime

from twistar.dbobject import DBObject

from coordinates import Coordinates


class Car(DBObject):
    @classmethod
    def tablename(cls):
        return 'cars'

    def report_itself(self):
        return "Car {}:\t{},{}\t({})".format(self.car_id, self.latitude,
                                             self.longitude, self.updated)

    @staticmethod
    def report(request):
        def _report(cars):
            if not cars:
                request.write('Car not found in the database.')
            else:
                request.write(cars[0].report_itself())
            request.finish()
        return _report

    @staticmethod
    def save_location(request, location):
        def _save_location(self):
            self.latitude = location.latitude
            self.longitude = location.longitude
            self.updated = datetime.datetime.now()
            self.save().addCallback(Car.report_ok(request))

        return _save_location

    @staticmethod
    def report_ok(request):
        def _report_ok(car):
            request.write("You data was successfully added. {}".format(car.report_itself()))
            request.finish()

        return _report_ok

    def distance(self, location):
        return location.distance(Coordinates(self.latitude, self.longitude))
