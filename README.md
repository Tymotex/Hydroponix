# Hydroponix
An IoT automated plant watering system using the Raspberry Pi Zero W. The working principle is simple — when the soil moisture sensor 

Components: 5-12V submersible DC motor, soil moisture sensor, 5V electromechanical relay module, humidity and temperature sensor (DHT22), USB 3.0 breakout boards, LCD1602 16x2 with I2C backpack, HC-SR501 passive infrared motion sensor
<Fritz schematic here>

### Currently implemented:
- All electronic components working with watering.py: soil moisture sensor can be successfully read, motor can be flicked on and off, humidity and ambient temperature can be read reliably
- Flask web app interface is able to fetch data from sensors, display camera module output and allow remote control over the water pump
- Enable/disable auto-watering and force water functionality working (using psutil to manage processes)
- Currently able to send HTTP post requests to timz.dev/Hydroponix and able to automate this process to send requests at regular intervals

### Work in progress and planned features:
- Set up InfluxDB to save sensor data snapshots at regular intervals
- Be able to pull average sensor readings each hour from the database and send that via an HTTP post 
- Use data visualisation libraries on sensor data

### Bugs:
- Humidity/temperature sensor is unable to successfully get both readings on every single call to the Adafruit_DHT.read function. Need to find a workaround -> ignore failed readings, take the average of the most recent 5 successful readings and return the recorded average where needed
