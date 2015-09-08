from collections import defaultdict


class Subscriber():
    subscribers = defaultdict(list)

    @classmethod
    def add(cls, car_id, request):
        cls.subscribers[car_id].append(request)

    @classmethod
    def get_subscribers(cls, car_id):
        return cls.subscribers[car_id]
