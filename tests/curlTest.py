import requests
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep

# Pins
tempHumidSensor = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def GetHumidityAndTemp():
	humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.AM2302, tempHumidSensor)
	if humidity is not None and temperature is not None:
		humidAndTemp = {
			'humidity' : round(humidity, 2),
			'temperature' : round(temperature, 2)
		}
		return humidAndTemp
	else:
		# On failure, retry
		print("Reattempting reading")
		return GetHumidityAndTemp()


weatherData = GetHumidityAndTemp()

URL = "https://timz.dev/Hydroponix"

data = {
    "title": "Snapshot From Pi Zero",
    "content": "The temperature is {} and the humidity is {}%".format(weatherData["temperature"], weatherData["humidity"])
}

# print(open("pic.png", "rb"))

files = {
    "photo": open("pic.jpg", "rb")
}

r = requests.post(url = URL, data = data, files = files)

print("==== Response ====")
print(r.text)
