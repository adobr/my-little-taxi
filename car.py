import datetime
from heapq import nsmallest

from twisted.internet.defer import Deferred
from twistar.dbobject import DBObject

from coordinates import Coordinates


def report_error(request):
    def _report_error(error):
        request.write("Something went wrong.")
        request.write(str(error))
        request.finish()
    return _report_error


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
            self.save().addCallbacks(Car.report_added(request),
                                     report_error(request))

        return _save_location

    @staticmethod
    def report_added(request):
        def _report_added(car):
            request.write("You data was successfully added. {}".format(car.report_itself()))
            request.finish()

        return _report_added

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

    @staticmethod
    def find_nearest(request, location, count):
        def _find_nearest(cars):
            d = Deferred()
            nearest_cars = nsmallest(count, cars, key=lambda car: car.distance(location))
            d.callback(nearest_cars)
            return d.addCallbacks(Car.report_nearest(request, location),
                                  report_error(request))
        return _find_nearest

