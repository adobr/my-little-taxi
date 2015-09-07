from heapq import nsmallest
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

    @staticmethod
    def find_nearest(request, location, count):
        def _find_nearest(cars):
            result = nsmallest(count, cars, key=lambda car: car.distance(location))
            Car.report_nearest(request, location)(result)

        return _find_nearest

    def distance(self, location):
        return location.distance(Coordinates(self.latitude, self.longitude))

    @staticmethod
    def report_nearest(request, location):
        def _report(cars):
            if not cars:
                request.write('We have no cars at all!')
            else:
                for car in cars:
                    request.write("{0}\t-\t{1:.2f}km\n".format(car.report_itself(),
                                                             car.distance(location)))
            request.finish()
        return _report