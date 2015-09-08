#!/usr/bin/env bash

CARS_COUNT=10000
REQUESTS_COUNT=1000

for i in {1..3}; do
    for request_type in get_car; do
        ./make_requests.py --cars_count=$CARS_COUNT --request_type $request_type \
         --requests_count=$REQUESTS_COUNT &
    done
done
