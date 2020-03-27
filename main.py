from time import time, sleep
import datetime
import sys
import requests
import Adafruit_DHT
import RPi.GPIO as GPIO
import os
import logging
import pprint
from influxdb import InfluxDBClient
from picamera import PiCamera

# Pins
tempHumidSensor = 4

# Config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

logging.basicConfig(level=logging.INFO)

# Reads the DHT22 hygrometer and returns a dictionary with keys: "humidity" and "temperature"
# Recursively calls itself on a failed reading
def GetHumidityAndTemp():
	humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.AM2302, tempHumidSensor)
	if humidity is not None and temperature is not None:
		humidAndTemp = {
			"humidity" : round(humidity, 2),
			"temperature" : round(temperature, 2)
		}
		return humidAndTemp
	else:
		# On failure, retry
		return GetHumidityAndTemp()

def InfluxWrite(weatherData):
    # InfluxDB writing and reading
    timestamp = int(time())
    jsonSensorBody = [
        {
            "measurement": "temperature_and_humidity",  # This is the table name
            "tags": {
                "temperature": weatherData["temperature"],   # These are the columns (attributes)
                "humidity": weatherData["humidity"]
            },
            "fields": {
                "value": 100  # Necessary to have something under "fields" (currently just a placeholder)
            }
        }
    ]
    # Connect to the influxDB instance running locally
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'hydroponix')
    # Write a data point into the influxDB instance
    client.write_points(jsonSensorBody, time_precision='ms') 
    
def InfluxRead(influxQuery):
    # Connect to the influxDB instance running locally
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'hydroponix')
    # Fetching the data back from the database (TODO: should do some preprocessing here. Eg. get the average over last 5 trials)
    result = client.query("select * from temperature_and_humidity;")
    dataPoints = list(result.get_points(measurement="temperature_and_humidity"))
    return dataPoints

def GetPhoto(camObject, picOutputPath):
    # Snapping a photo of the setup
    camObject.vflip = False   # Fixes incorrect vertical orientation
    camObject.resolution = (1024, 768)
    camObject.start_preview(alpha=192)
    sleep(1)  # Allow buffer time
    camObject.capture(picOutputPath)
    camObject.stop_preview()

def HTTPPost(postURL, picPath, weatherData):
    postDataBody = {
        "title": "Snapshot From Pi Zero",
        "content": "The temperature is {} and the humidity is {}%".format(weatherData["temperature"], weatherData["humidity"])
    }
    postFiles = {
        "photo": open(picPath, "rb")
    }
    r = requests.post(url = postURL, data = postDataBody, files = postFiles)

def SendDataSnapshot(cameraObject):
    # Get the weather data
    weatherData = GetHumidityAndTemp()
        
    # Writes the current data snapshot into influxdb and fetches back a list of datapoints
    InfluxWrite(weatherData)
    dataPoints = InfluxRead("SELECT * FROM temperautre_and_humidity")

    # Getting a physical photo through the camera module
    picPath = "pic.jpg"
    GetPhoto(cameraObject, picPath)

    # Making the HTTP POST request to /Hydroponix to upload a new data snapshot to the mongo database
    postURL = "https://timz.dev/Hydroponix"
    HTTPPost(postURL, picPath, weatherData)

    for eachPoint in dataPoints:
        pass
        # pprint.pprint(eachPoint, width=1)    # TODO: should only print latest 10 datapoints fetched from influxdb
    os.remove("pic.jpg")  # Removing the snapped picture

   
if __name__ == "__main__":
    snapshotInterval = 0
    if (len(sys.argv) > 1):  # Command line input handling should be more robust. TODO: look at more examples of how this is done
        snapshotInterval = int(sys.argv[1])
    else:
        sys.stdout.write("Setting snapshot interval to default (2 hours)")
        snapshotInterval = 7200
    try:
        camera = PiCamera()
        while (True):
            logging.info("Sending a data snapshot now! (interval is {0})".format(snapshotInterval))
            SendDataSnapshot(camera)
            sleep(snapshotInterval)
    except KeyboardInterrupt:
        try:
            logging.info("Cleaning up")
            os.remove("pic.jpg")  # Removing the snapped picture
        except FileNotFoundError:
            pass



