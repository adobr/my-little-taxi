#!/usr/bin/env python

import sys
import time
from twisted.web import server, resource
from twisted.enterprise import adbapi
from twisted.internet import reactor
from twistar.registry import Registry
from twistar.dbobject import DBObject

from coordinates import Coordinates


class CarResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        # TODO: move it to POST
        car_id = int(request.args['id'][0])
        location = Coordinates(request.args['ll'][0])
        car = Car(car_id=car_id, latitude=location.latitude,
                  longitude=location.longitude, updated=time.time()) # TODO: fix timestamp
        car.findOrCreate().addCallback(done)
        return "Car is added."

    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        car_id = request.args.get('id')
        print(car_id)
        return "Data was successfully added."


class NearestCarsResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        #TODO: add real logic
        Car.all().addCallback(printAll)
        return "No cars now."



class HelpResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        docs = """
Welcome to MyLittleTaxi app.
Here is the rest api:
    GET /cars?id=42                                 - get car location
    POST /cars?id=42&ll=55.75222,37.61556           - set car location
    GET /nearest_cars?ll=55.75222,37.61556&count=11 - get nearest cars
"""
        return docs


class Car(DBObject):
    @classmethod
    def tablename(cls):
        return 'cars'


def done(car):
    print car
    print car.errors
    print "A car was just created  %s" % car.id


def printAll(all):
    print 'printing: %s' % all

def main():
    #from twisted.python import log
    #log.startLogging(sys.stdout)

    root = resource.Resource()
    root.putChild("help", HelpResource())
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