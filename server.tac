# You can run this .tac file directly with:
#    twistd -ny server.tac


from twisted.web import server, resource
from twistar.dbconfig.mysql import ReconnectingMySQLConnectionPool
from twisted.application import service, internet
from twistar.registry import Registry
from twisted.python.logfile import DailyLogFile


from coordinates import Coordinates
from car import Car, report_error


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
        # TODO: send info until connection is broken
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


def get_web_service():
    #from twisted.python import log
    #log.startLogging(sys.stdout)

    root = resource.Resource()
    root.putChild("car", CarResource())
    root.putChild("nearest_cars", NearestCarsResource())

    # Connect to the DB
    Registry.DBPOOL = ReconnectingMySQLConnectionPool('MySQLdb', user="little_server",
                                                      passwd="ne6rexeT", db="little_taxi",
                                                      cp_reconnect=True, cp_max=10)

    # Create server
    web_server = server.Site(root)
    return internet.TCPServer(8090, web_server)

application = service.Application("Demo application")
logfile = DailyLogFile("little_taxi.log", ".")
service = get_web_service()
service.setServiceParent(application)