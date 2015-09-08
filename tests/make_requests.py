#!/usr/bin/env python

import requests
import random
import argparse
import time

CAR_URL = "http://localhost:8090/car"
NEAREST_CAR_URL = "http://localhost:8090/nearest_cars"


class Requester():
    def __init__(self, cars_count, verbose):
        self.cars_count = cars_count
        self.verbose = verbose

    def get_random_car_id(self):
        return random.randint(1, self.cars_count)

    def get_random_count(self):
        return random.randint(1, 100)

    def get_random_ll(self):
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        return "{},{}".format(latitude, longitude)

    def make_get_car_request(self):
        url = "{}?car_id={}".format(CAR_URL, self.get_random_car_id())
        r = requests.get(url)
        if self.verbose:
            print r.text
            print

    def make_post_car_request(self):
        url = "{}?car_id={}&ll={}".format(CAR_URL,
                                          self.get_random_car_id(),
                                          self.get_random_ll())
        r = requests.post(url)
        if self.verbose:
            print r.text
            print

    def make_get_nearest_request(self):
        url = "{}?ll={}&count={}".format(NEAREST_CAR_URL,
                                         self.get_random_ll(),
                                         self.get_random_count())
        r = requests.get(url)
        if self.verbose:
            print r.text
            print


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cars_count", type=int, default=100)
    parser.add_argument("--request_type", default="post_car",
                        help="(get_car/post_car/get_nearest)")
    parser.add_argument("--requests_count", type=int, default=100)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)

    args = parser.parse_args()
    requester = Requester(cars_count=args.cars_count, verbose=args.verbose)
    start = time.time()
    print "Starting {} {} requests".format(args.requests_count,
                                           args.request_type)
    for i in xrange(args.requests_count):
        if args.request_type == "get_car":
            requester.make_get_car_request()
        elif args.request_type == "get_nearest":
            requester.make_get_nearest_request()
        elif args.request_type == "post_car":
            requester.make_post_car_request()
        else:
            raise Exception("Incorrect request_type {}".format(args.request_type))
    print("{0} {1} requests in {2:.2f} seconds".format(args.requests_count,
                                                       args.request_type,
                                                       time.time() - start))

if __name__ == "__main__":
    main()