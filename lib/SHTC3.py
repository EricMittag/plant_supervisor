#Temperature and Humidity Sensor on RPi Sense HAT

import time
import board
import adafruit_shtc3

i2c = board.I2C()  # uses board.SCL and board.SDA
sht = adafruit_shtc3.SHTC3(i2c)

def getTemperature():
  return round(sht.temperature,1)

def getHumidity():
  return sht.relative_humidity

def testing():
  print("TEST: SHTC3\n")

  while True:
    temperature = getTemperature()
    relative_humidity = getHumidity()
    print('Temperature = {}°C , Humidity = {}%'.format(temperature, relative_humidity))
    time.sleep(1)


if __name__ == "__main__":
  testing()