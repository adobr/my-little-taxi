#!/usr/bin/env bash

CARS_COUNT=10000
REQUESTS_COUNT=100
STREAMS_COUNT=2

for i in `seq $STREAMS_COUNT`; do
    for request_type in get_car post_car get_nearest; do
        ./tests/make_requests.py --cars_count=$CARS_COUNT --request_type $request_type \
         --requests_count=$REQUESTS_COUNT &
    done
done

wait
