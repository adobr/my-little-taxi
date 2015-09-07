CREATE DATABASE IF NOT EXISTS little_taxi;
USE little_taxi;
CREATE TABLE cars (
    id INT PRIMARY KEY AUTO_INCREMENT,
    car_id VARCHAR(10),
    latitude FLOAT,
    longitude FLOAT,
    updated TIMESTAMP);
CREATE USER 'little_server'@'localhost' IDENTIFIED BY 'ne6rexeT';
GRANT ALL ON little_taxi.* TO 'little_server'@'localhost';
