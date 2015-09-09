my-little-taxi
==============
Small twisted web server

Install requirements
-------------------
sudo apt-get install mysql-server python-mysqldb

sudo pip install -r requirements.txt

Init database
--------------
mysql -u root < init_db.sql
(add -p if you have set a password to mysql during installation)

Start server
------------
twistd -ny server.tac --logfile=server.log

Usage
-----
* set car location

curl --request POST 'http://localhost:8090/car?car_id=42&ll=37.412021,11.896277'

* get car location

curl --request GET  'http://localhost:8090/car?car_id=42'

* subscribe to car location updates

curl  --no-buffer --request GET  'http://localhost:8090/subscribe?car_id=42'

* get nearest cars

curl --request GET 'http://localhost:8090/nearest_cars?ll=37.412021,11.896277&count=11'

Testing
-------
* simple performance test

tests/make_requests.sh

* simple functional tests

py.test tests/functional.py