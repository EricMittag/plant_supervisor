#!/bin/bash

echo 'Starting Routines for Sensor Data and Webserver';

sudo nohup python main_sensor_data.py > log/log_sensors.txt 2>&1&
sudo nohup python main_webserver.py > log/log_webserver.txt 2>&1&