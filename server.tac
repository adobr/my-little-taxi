# You can run this .tac file directly with:
#    twistd -ny server.tac

from twisted.web import server, resource
from twistar.dbconfig.mysql import ReconnectingMySQLConnectionPool
from twisted.application import service, internet
from twistar.registry import Registry


from coordinates import Coordinates
from car import Car
from report import Report
from subscriber import Subscriber


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
    """
        GET: get car by id
        POST: post car location
    """
    isLeaf = True

    def render_GET(self, request):
        try:
            (car_id,) = parse_args(request, ['car_id'])
        except Exception as e:
            return e.message
        d = Car.findBy(car_id=car_id)
        d.addCallback(Report(request).report_found_cars)
        d.addErrback(Report(request).report_error)
        return server.NOT_DONE_YET

    def render_POST(self, request):
        try:
            (car_id, ll) = parse_args(request, ['car_id', 'll'])
            location = Coordinates.from_string(ll)
        except Exception as e:
            return e.message
        d = Car.findOrCreate(car_id=car_id)
        d.addCallback(Car.save_location(request, location))
        d.addErrback(Report(request).report_error)
        return server.NOT_DONE_YET


class SubscribeResource(resource.Resource):
    """
        GET: subscribe to car location updates by id
        the data will be pushed until connection is closed
    """
    isLeaf = True

    def render_GET(self, request):
        try:
            (car_id,) = parse_args(request, ['car_id'])
        except Exception as e:
            return e.message
        d = Car.findBy(car_id=car_id)
        d.addCallback(Report(request, close_connection=False).report_found_cars)
        d.addErrback(Report(request).report_error)
        Subscriber.add(car_id, request)
        return server.NOT_DONE_YET


class NearestCarsResource(resource.Resource):
    """
        GET: find N nearest cars
    """
    isLeaf = True

    def render_GET(self, request):
        try:
            (ll, count) = parse_args(request, ['ll', 'count'])
            count = int(count)
        except Exception as e:
            return e.message
        location = Coordinates.from_string(ll)
        d = Car.all()
        d.addCallback(Car.find_nearest(request, location, count))
        d.addErrback(Report(request).report_error)
        return server.NOT_DONE_YET


def get_web_service():
    root = resource.Resource()
    root.putChild("car", CarResource())
    root.putChild("subscribe", SubscribeResource())
    root.putChild("nearest_cars", NearestCarsResource())

    Registry.DBPOOL = ReconnectingMySQLConnectionPool('MySQLdb', user="little_server",
                                                      passwd="ne6rexeT", db="little_taxi",
                                                      cp_reconnect=True, cp_max=10)
    web_server = server.Site(root)
    return internet.TCPServer(8090, web_server)


application = service.Application("Little server")
service = get_web_service()
service.setServiceParent(application)