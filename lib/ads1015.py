# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

# Get Voltage of one ADC Channel (0-3) in mV
def getChannelVoltage(channel):
    value = adc.read_adc(channel, gain=1)
    voltage = value*2 #For ADS1115: (value/32767)*4096
    return int(round(voltage))


def testing():
  print("TEST: ADS1015\n")

  while True:
    print('| {0:<10}| {1:<10}| | {2:<10}| {3:<10}|'.format(round(getChannelVoltage(0), 3), round(getChannelVoltage(1), 3), round(getChannelVoltage(2), 3), round(getChannelVoltage(3), 3)))
    time.sleep(1)


if __name__ == "__main__":
  testing()
  