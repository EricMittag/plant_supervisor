#Webserver

from flask import Flask, render_template
import os
import time
import picamera
import csv
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

#Camera
def takeImageOfPlant():
  camera = picamera.PiCamera()
  camera.resolution = (1280, 720)
  #camera.rotation = 180
  camera.start_preview()
  time.sleep(2) # Camera warm-up time
  camera.capture('static/plant_new.jpg')
  print("--New image of plant taken--")
  camera.stop_preview()
  camera.close()

@app.route("/")
def default():
  #Load sensor data from CSV file
  with open('Sensor_Data.csv', "r") as f:
    lastrow = list(csv.reader(f))[-1]
    updateTime = lastrow[0]
    temper = lastrow[1]
    press = lastrow[2]
    hum = lastrow[3]
    soilmois = lastrow[4]
    water = lastrow[-1]
    f.close()
  return render_template('index.html', time=updateTime, temperature=temper, pressure=press, humidity=hum, soilmoisture=soilmois, lastWater=water)

@app.route("/test")
def test():
  return "Just for Testing"

@app.route("/newImg")
def newImg():
  takeImageOfPlant()
  return render_template('newImage.html')

@app.route("/imgGal")
def imgGal():
  listOfElementsInIMGFolder = sorted(os.listdir('static/img'))
  #Exclude all other Elements in Folder which are not images
  imageList = ['img/' + i for i in listOfElementsInIMGFolder if i.startswith('plant_')]

  return render_template('imgGalery.html', imagesOnServer=imageList)

@app.route("/stats")
def stats():
  df = pd.read_csv('Sensor_Data.csv')
  fig_temperature = px.line(df, x='timestamp', y='temperature', title='Temperature')
  fig_humidity = px.line(df, x='timestamp', y='humidity', title='Humidity')
  fig_moisture = px.line(df, x='timestamp', y='mois', title='Soil Moisture')

  graphJSON_t = json.dumps(fig_temperature, cls=plotly.utils.PlotlyJSONEncoder)
  graphJSON_h = json.dumps(fig_humidity, cls=plotly.utils.PlotlyJSONEncoder)
  graphJSON_m = json.dumps(fig_moisture, cls=plotly.utils.PlotlyJSONEncoder)

  return render_template('stats.html', graphJSON_t=graphJSON_t, graphJSON_h=graphJSON_h, graphJSON_m=graphJSON_m)

def main():
  print("MAIN: Webserver\n")

  app.run(host="::", port=80, debug=False)


if __name__ == "__main__":
  main()