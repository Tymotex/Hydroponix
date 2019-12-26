import RPi.GPIO as GPIO
import Adafruit_DHT
from time import sleep

isEnabled = True

# Pins
relayTrigger = 21
moistureSensor = 20
statusLED = 16
tempHumidSensor = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayTrigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(moistureSensor, GPIO.IN)
GPIO.setup(statusLED, GPIO.OUT, initial=GPIO.LOW)

def on(pin):
    GPIO.output(pin, GPIO.HIGH)

def off(pin):
    GPIO.output(pin, GPIO.LOW)

def GetHumidityAndTemp():
	humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.AM2302, tempHumidSensor)
	if humidity is not None and temperature is not None:
		humidAndTemp = {
			'humidity' : humidity,
			'temperature' : temperature
		}
		return humidAndTemp
	else:
		# On failure, return a dictionary with zeroed values
		# TODO: Need better error-handling
		return {
			'humidity' : 0,
			'temperature' : 0
		}

if __name__ == '__main__':
	while True:
		print("=== Looping ===")
		if GPIO.input(moistureSensor):
			print("Dry")
			off(relayTrigger)
			off(statusLED)
		else:
			print("Wet")
			on(relayTrigger)
			on(statusLED)
		
		data = GetHumidityAndTemp()
		print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(data["temperature"], data["humidity"]))	
		
		sleep(1)



def GetLastWatered():
	print("===> Getting last watered")
	return "Never!"
