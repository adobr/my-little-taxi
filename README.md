# my-little-taxi
Small twisted web server

apt-get install mysql-service python-mysqldb
pip install -r requirements.txt

# start database
sudo mysqld --datadir /home/dobrokhotova/msqldata -p 8070 --init-file init_db.sql

python server.py

wget "localhost:8090/help"
