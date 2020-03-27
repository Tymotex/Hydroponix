import RPi.GPIO as GPIO
import Adafruit_DHT
from time import sleep
import logging

isEnabled = True

# ===== Pins =====
relayTrigger = 21
moistureSensor = 20
statusLED = 16
tempHumidSensor = 4

# ===== Configuration =====
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayTrigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(moistureSensor, GPIO.IN)
GPIO.setup(statusLED, GPIO.OUT, initial=GPIO.LOW)

logging.basicConfig(level=logging.INFO)

def ForceWater(forceInterval):
    """ Force activate the pump for a specified time interval """
    GPIO.output(relayTrigger, GPIO.LOW)
    GPIO.output(statusLED, GPIO.HIGH)
    sleep(forceInterval)
    GPIO.output(relayTrigger, GPIO.HIGH)
    GPIO.output(statusLED, GPIO.LOW)

def ResetState():
    GPIO.output(relayTrigger, GPIO.HIGH)
    GPIO.output(statusLED, GPIO.HIGH)

def AutoWater(checkInterval):
    while isEnabled:
        if GPIO.input(moistureSensor):
            logging.info("Low moisture level")
            GPIO.output(relayTrigger, GPIO.LOW)
            GPIO.output(statusLED, GPIO.LOW)
        else:
            logging.info("High moisture level")
            GPIO.output(relayTrigger, GPIO.HIGH)
            GPIO.output(statusLED, GPIO.HIGH)
        sleep(checkInterval)

if __name__ == '__main__':
   AutoWater(1)

