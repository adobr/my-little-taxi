from twisted.web import server, resource
from twisted.internet import reactor

from coordinates import Coordinates


class CarResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        car_id = request.args.get('car')
        print(car_id)

        return "Your car is here: ."

    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        car_id = request.args.get('id')
        print(car_id)
        return "Data was successfully added."


class NearestCarsResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
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

root = resource.Resource()
root.putChild("help", HelpResource())
root.putChild("car", CarResource())
root.putChild("nearest_cars", NearestCarsResource())
reactor.listenTCP(80, server.Site(root))
reactor.run()
