my-little-taxi
==============
Small twisted web server

Install requirements
-------------------

apt-get install mysql-server python-mysqldb

pip install -r requirements.txt

Start database
--------------
sudo mysqld --init-file init_db.sql

Start server
------------
twistd -ny server.tac --logfile=server.log

Usage
-----
* set car location

curl --request POST 'http://localhost:8090/car?id=42&ll=37.412021,11.896277'

* get car location

curl --request GET  'http://localhost:8090/car?id=42'

* subscribe to car location updates

curl --request GET  'http://localhost:8090/subscribe?id=42' --no-buffer

* get nearest cars

curl --request GET 'http://localhost:8090/nearest_cars?ll=37.412021,11.896277&count=11'

Testing
-------
* simple performance test

tests/make_requests.sh

* simple functional tests

py.test tests/functional.py