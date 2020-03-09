from time import time, sleep
import datetime
import sys
import requests
import Adafruit_DHT
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
from picamera import PiCamera

# Pins
tempHumidSensor = 4

# Config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

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

weatherData = GetHumidityAndTemp()

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
# client.write_points(jsonSensorBody, time_precision='ms') 
# Fetching the data back from the database (TODO: should do some preprocessing here. Eg. get the average over last 5 trials)
result = client.query("select * from temperature_and_humidity;")
dataPoints = list(result.get_points(measurement="temperature_and_humidity"))

# Snapping a photo of the setup
picPath = "pic1.jpg"
camera = PiCamera()
camera.vflip = True  # Fixes incorrect vertical orientation
camera.resolution = (1024, 768)
camera.start_preview(alpha=192)
sleep(1) # Allow buffer time
camera.capture(picPath)
camera.stop_preview()

# Making the HTTP POST request to /Hydroponix to upload a new data snapshot to the mongo database
URL = "https://timz.dev/Hydroponix"
data = {
    "title": "Snapshot From Pi Zero",
    "content": "The temperature is {} and the humidity is {}%".format(weatherData["temperature"], weatherData["humidity"])
}
files = {
    "photo": open(picPath, "rb")
}
r = requests.post(url = URL, data = data, files = files)



