#!/usr/bin/env python

import requests
import random
import argparse
import time


class Requester():
    def __init__(self, cars_count, verbose, host="localhost", port=8090):
        self.cars_count = cars_count
        self.verbose = verbose
        self.car_url = "http://{}:{}/car".format(host, port)
        self.nearest_car_url = "http://{}:{}/nearest_cars".format(host, port)

    def get_random_car_id(self):
        return random.randint(1, self.cars_count)

    def get_random_count(self):
        return random.randint(1, 100)

    def get_random_ll(self):
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        return "{},{}".format(latitude, longitude)

    def make_get_car_request(self):
        url = "{}?car_id={}".format(self.car_url, self.get_random_car_id())
        r = requests.get(url)
        if self.verbose:
            print r.text
            print

    def make_post_car_request(self):
        url = "{}?car_id={}&ll={}".format(self.car_url,
                                          self.get_random_car_id(),
                                          self.get_random_ll())
        r = requests.post(url)
        if self.verbose:
            print r.text
            print

    def make_get_nearest_request(self):
        url = "{}?ll={}&count={}".format(self.nearest_car_url,
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
    print "Starting {} {} requests...".format(args.requests_count,
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