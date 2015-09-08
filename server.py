#!/usr/bin/env python

from twisted.web import server, resource
from twisted.enterprise import adbapi
from twisted.internet import reactor
from twistar.registry import Registry

from coordinates import Coordinates
from car import Car


def report_error(request):
    def _report_error(error):
        request.write("Something went wrong.")
        request.write(str(error))
        request.finish()
    return _report_error


def parse_args(request, required):
    result = []
    for param in required:
        if not request.args.get(param):
            raise Exception("Parameter {} is required.".format(param))
        if len(request.args[param]) != 1:
            raise Exception("Parameter {} should be unique.".format(param))
        result.append(request.args[param][0])
    return result


class CarResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        try:
            (car_id,) = parse_args(request, ['car_id'])
        except Exception as e:
            return e.message
        Car.findBy(car_id=car_id).addCallbacks(Car.report(request),
                                               report_error(request))
        return server.NOT_DONE_YET

    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        try:
            (car_id, ll) = parse_args(request, ['car_id', 'll'])
            location = Coordinates.from_string(ll)
        except Exception as e:
            return e.message
        Car.findOrCreate(car_id=car_id).addCallbacks(Car.save_location(request, location),
                                                     report_error(request))
        return server.NOT_DONE_YET


class NearestCarsResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        try:
            (ll, count) = parse_args(request, ['ll', 'count'])
            count = int(count)
        except Exception as e:
            return e.message
        location = Coordinates.from_string(ll)
        Car.all().addCallbacks(Car.find_nearest(request, location, count),
                               report_error(request))
        return server.NOT_DONE_YET


def main():
    #from twisted.python import log
    #log.startLogging(sys.stdout)

    root = resource.Resource()
    root.putChild("car", CarResource())
    root.putChild("nearest_cars", NearestCarsResource())

    # Connect to the DB
    Registry.DBPOOL = adbapi.ConnectionPool('MySQLdb', user="little_server",
                                            passwd="ne6rexeT", db="little_taxi")

    # Start reactor
    reactor.listenTCP(8090, server.Site(root))
    reactor.run()

if __name__ == '__main__':
    main()