import datetime
from heapq import nsmallest

from twisted.internet.defer import Deferred
from twistar.dbobject import DBObject

from coordinates import Coordinates
from report import Report
from subscriber import Subscriber


class Car(DBObject):
    @classmethod
    def tablename(cls):
        return 'cars'

    def __str__(self):
        return "#{}: {},{} ({})".format(self.car_id.zfill(5), self.latitude,
                                        self.longitude, self.updated)

    @staticmethod
    def save_location(request, location):
        def _save_location(self):
            self.latitude = location.latitude
            self.longitude = location.longitude
            self.updated = datetime.datetime.now()
            d = self.save()
            d.addCallback(Car.report_updated_data(request))
            d.addErrback(Report(request).report_error)

        return _save_location

    @staticmethod
    def report_updated_data(request):
        def _report_updated_data(self):
            Report(request).report_added_car(self)
            for subscriber in Subscriber.get_subscribers(self.car_id):
                Report(subscriber, close_connection=False).report_to_subscriber(self)

        return _report_updated_data

    def distance(self, location):
        return location.distance(Coordinates(self.latitude, self.longitude))

    @staticmethod
    def find_nearest(request, location, count):
        def _find_nearest(cars):
            d = Deferred()
            nearest_cars = nsmallest(count, cars, key=lambda c: c.distance(location))
            result = []
            for car in nearest_cars:
                result.append((car, car.distance(location)))
            d.callback(result)
            return d.addCallbacks(Report(request).report_nearest_cars,
                                  Report(request).report_error)
        return _find_nearest

