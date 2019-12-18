import RPi.GPIO as GPIO
from time import sleep

# Pins
relayTrigger = 21
moistureSensor = 20
statusLED = 16   

GPIO.setmode(GPIO.BCM)
GPIO.setup(relayTrigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(moistureSensor, GPIO.IN)
GPIO.setup(statusLED, GPIO.OUT, initial=GPIO.LOW)

def on(pin):
    GPIO.output(pin, GPIO.HIGH)

def off(pin):
    GPIO.output(pin, GPIO.LOW)

if __name__ == '__main__':
    while True:
        print("=== Looping ===")
        if GPIO.input(moistureSensor):
            print("Dry")
            relayOff(relayTrigger)
            off(statusLED)
        else:
            print("Wet")
            relayOn(relayTrigger)
            on(statusLED)
        sleep(1)
