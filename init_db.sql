CREATE DATABASE IF NOT EXISTS little_taxi;
USE little_taxi;
CREATE TABLE cars (
    car_id INT PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    updated TIMESTAMP);
CREATE USER 'little_server'@'localhost' IDENTIFIED BY 'ne6rexeT';
GRANT ALL ON little_taxi.* TO 'little_server'@'localhost';
