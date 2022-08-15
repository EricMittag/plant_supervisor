#ground humidity sensor

#imports
import time
from lib import ads1015
import numpy

#Convert Moisture Sensor voltage to Moisture Percentage
def moistureVoltageToPercentage(voltage):
  sensorMinMax = [1330, 2780] #Voltages measured via Air and Water
  percentage = [0, 100]

  return round(100-numpy.interp(voltage, sensorMinMax, percentage),1)

#Get moisture in Percentage
def moisturePercentage():
  return moistureVoltageToPercentage(ads1015.getChannelVoltage(0))


def testing():
  print("TEST: SoilMoisture\n")

  while True:
    mois = moisturePercentage()
    print('Soil Moisture: {}%'.format(mois))
    time.sleep(1)


if __name__ == "__main__":
  testing()