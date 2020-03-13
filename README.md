# Hydroponix
An IoT automated plant propagation system built with Python on the Raspberry Pi Zero W with influxDB, Flask, Bootstrap 4, requests, psutil, Adafruit_DHT, picamera and more.

Components: 5-12V submersible DC motor, soil moisture sensor, 5V electromechanical relay module, humidity and temperature sensor (DHT22), USB 3.0 breakout boards, LCD1602 16x2 with I2C backpack, HC-SR501 passive infrared motion sensor
<Fritz schematic here>

### Currently implemented:
- All electronic components working with watering.py: soil moisture sensor can be successfully read, motor can be flicked on and off, humidity and ambient temperature can be read reliably
- Flask web app interface is able to fetch data from sensors, display camera module output and allow remote control over the water pump
- Enable/disable auto-watering and force water functionality working (using psutil to manage processes)
- Currently able to send HTTP post requests to timz.dev/Hydroponix and able to automate this process to send requests at regular intervals
- Automated HTTP POST requests is working and able to send image files and sensor data to timz.dev/Hydroponix

### Work in progress and planned features:
- Sending snapshots at regular intervals is currently disabled. Need to fix the paths to have a designated camera output folder and manage local dependencies (LCDDriver)
- Be able to pull average sensor readings each hour from the database
- Use data visualisation libraries on sensor data
- Use threading's Timer object to delegate LCD writing

### Bugs:
- Humidity/temperature sensor is unable to successfully get both readings on every single call to the Adafruit_DHT.read function. The current workaround is to use a recursive function and recall until success. Could alternatively just take the average of the most recent 5 readings, for example
