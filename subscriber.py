from collections import defaultdict


class Subscriber():
    subscribers = defaultdict(list)

    @classmethod
    def add(cls, car_id, request):
        request.notifyFinish().addErrback(cls.remove_subscriber(car_id, request))
        cls.subscribers[car_id].append(request)

    @classmethod
    def get_subscribers(cls, car_id):
        return cls.subscribers[car_id]

    @classmethod
    def remove_subscriber(cls, car_id, request):
        def _remove_subscriber(error):
            cls.subscribers[car_id].remove(request)

        return _remove_subscriber

