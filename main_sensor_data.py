#Sensor Data

#Imports
import RPi.GPIO as GPIO
import time
from datetime import datetime
import csv
import picamera

from lib import SHTC3
from lib import LPS22HB
from lib import soilMoisture


if __name__ == "__main__":
  print("MAIN: Sensor Data")

################################################################
#Setup Variables and Pins

#Counter for smoothing faulty sensor readings
activateWaterCounter = 0

###########
#PARAMETERS
#Temperature Offset
TEMPERATURE_OFFSET = -7.6
#Goal Moisture Percentage
GOAL_MOISTURE = 40

lastTimeWatering = 0

#Setput Indicator LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(27, GPIO.LOW)
time.sleep(0.5)
GPIO.output(27, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(27, GPIO.LOW)

#Setup Water Pump Pin
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

#############################################################
#Functions 

#activate Pump for a specific time (in s)
def activatePump(seconds):
  GPIO.output(17, True)
  time.sleep(seconds)
  GPIO.output(17, False)

#Camera
def takeImageOfPlant(counter):
  camera = picamera.PiCamera()
  camera.resolution = (1280, 720)
  #camera.rotation = 180
  camera.start_preview()
  time.sleep(2) # Camera warm-up time
  path = ('static/img/plant_{}.jpg').format(counter)
  camera.capture(path)
  print("--New image of plant taken--")
  print(path)
  camera.stop_preview()
  camera.close()

#############################################################
#MAIN LOOP
while True:
  #Update Sensors
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  temperature = round(SHTC3.getTemperature() + TEMPERATURE_OFFSET,1)
  pressure = LPS22HB.getPressure()
  humidity = SHTC3.getHumidity()
  mois = soilMoisture.moisturePercentage()
  #Last time when Plant got watered -> get from Database
  with open('Sensor_Data.csv', "r") as f:
    lastrow = list(csv.reader(f))[-1]
    lastTimeWatering = lastrow[-1]
    f.close()

  ###########################################################
  #Watering Routine
  if mois < GOAL_MOISTURE:
    activateWaterCounter += 1
  else:
    activateWaterCounter = 0

  print("Counter: {}".format(activateWaterCounter))

  #Activate Pump if threshold and counter limit is reached
  if activateWaterCounter == 10:
    print("Watering Plant")
    activatePump(2) #for 2 seconds
    lastTimeWatering = timestamp
    activateWaterCounter = 0

  ############################################################
  #Save sensor data to CSV file
  datastring = [timestamp, temperature, pressure, humidity, mois, lastTimeWatering]
  with open('Sensor_Data.csv', "a", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(datastring)
    f.close()
  
  ############################################################
  #Take Snapchot once a day at 14:00
  date = datetime.now().today().strftime("%Y%m%d")
  hour = datetime.now().hour
  minute = datetime.now().minute 

  if hour==14 and minute <=5:
    takeImageOfPlant(date)

  #sleep for 5 Min
  time.sleep(60*5)

