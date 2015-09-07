from twisted.internet.defer import Deferred

from heapq import nsmallest


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


def find_nearest(request, location, count):
    def _find_nearest(cars):
        d = Deferred()
        # TODO: use it
        result = nsmallest(count, cars, key=lambda car: car.distance(location))
        report_nearest(request, location)(result)

    return _find_nearest





