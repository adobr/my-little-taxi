#!/usr/bin/env python

from twisted.web import server, resource
from twisted.enterprise import adbapi
from twisted.internet import reactor
from twistar.registry import Registry

from coordinates import Coordinates
from car import Car
from nearest import find_nearest


def report_error(request):
    def _report_error(error):
        request.write("Something went wrong.")
        request.finish()
    return _report_error


class CarResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        car_id = int(request.args['id'][0])
        Car.findBy(car_id=car_id).addCallbacks(Car.report(request),
                                               report_error(request))
        return server.NOT_DONE_YET

    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        car_id = int(request.args['id'][0])
        location = Coordinates.from_string(request.args['ll'][0])
        Car.findOrCreate(car_id=car_id).addCallbacks(Car.save_location(request, location),
                                                     report_error(request))
        return server.NOT_DONE_YET


class NearestCarsResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        location = Coordinates.from_string(request.args['ll'][0])
        count = int(request.args['count'][0])
        Car.all().addCallbacks(find_nearest(request, location, count),
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