from time import time, sleep
import statistics
import datetime
import sys
import requests
import Adafruit_DHT
import RPi.GPIO as GPIO
import os
import logging
import argparse
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
    result = client.query(influxQuery)
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

def HTTPPost(postURL, picPath, weatherData, snapshotTitle):
    postDataBody = {
        "title": snapshotTitle,
        "content": "The temperature is {}°C and the humidity is {}%.".format(weatherData["temperature"], weatherData["humidity"])
    }
    postFiles = {
        "photo": open(picPath, "rb")
    }
    r = requests.post(url = postURL, data = postDataBody, files = postFiles)

def SendDataSnapshot(cameraObject, snapshotTitle):
    # Get the weather data
    weatherData = GetHumidityAndTemp()
        
    # Writes the current data snapshot into influxdb and fetches back a list of datapoints
    InfluxWrite(weatherData)
    result = InfluxRead('''
        SELECT * FROM temperature_and_humidity ORDER BY "time" LIMIT 25;
    ''')
    
    compiledTemp = []
    compiledHumidity = []
    for datapoint in result:
        compiledTemp.append(float(datapoint["temperature"]))
        compiledHumidity.append(float(datapoint["humidity"]))

    medHumidity = statistics.median(compiledTemp)
    medTemp = statistics.median(compiledHumidity)
    avgHumidity = statistics.mean(compiledTemp)
    avgTemp = statistics.mean(compiledHumidity)
    logging.info("""
        ===== Latest 25 data snapshot stats =====
        Mean humidity: {}%, 
        Mean temperature: {}°C,
        Median humidity: {}%
        Meadian temperature: {}°C
    """.format(avgHumidity, avgTemp, medHumidity, medTemp))

    # Getting a physical photo through the camera module
    picPath = "pic.jpg"
    GetPhoto(cameraObject, picPath)

    # Making the HTTP POST request to /Hydroponix to upload a new data snapshot to the mongo database
    postURL = "https://timz.dev/Hydroponix"
    HTTPPost(postURL, picPath, weatherData, snapshotTitle)

    #for eachPoint in dataPoints:
    #    pass
        # pprint.pprint(eachPoint, width=1)    # TODO: should only print latest 10 datapoints fetched from influxdb
    os.remove("pic.jpg")  # Removing the snapped picture

   
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="CLI for sending data snapshot", epilog="Happy hacking :)")
    arg_parser.add_argument("-o", "--oneshot",
                            action="store_true",
                            help="Send once and terminate afterwards")
    arg_parser.add_argument("-a", "--auto-interval",
                            action="store",
                            help="Send regular snapshots at a specified time interval",
                            type=int,
                            nargs=1,
                            default=3600)
    arg_parser.add_argument("snapshot_title",
                            metavar="snapshot_title",
                            type=str,
                            help="Title of this snapshot")
    args = arg_parser.parse_args()
    
    snapshotInterval = args.auto_interval[0] if isinstance(args.auto_interval, list) else args.auto_interval
    snapshotTitle = args.snapshot_title
    try:
        camera = PiCamera()
        while (True):
            logging.info("Sending a data snapshot now! (interval is {0})".format(snapshotInterval))
            SendDataSnapshot(camera, snapshotTitle)
            if (args.oneshot):
                logging.info("Oneshot mode was true. Quitting")
                break
            sleep(snapshotInterval)
    except KeyboardInterrupt:
        try:
            logging.info("Cleaning up")
            os.remove("pic.jpg")  # Removing the snapped picture
        except FileNotFoundError:
            pass

