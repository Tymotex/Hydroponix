# Hydroponix
An IoT automated plant watering system using the Raspberry Pi Zero W. The working principle is simple — when the soil moisture sensor 

Components used: 5-12V submersible DC motor, soil moisture sensor, electromechanical relay module, humidity and temperature sensor (DHT22), USB 3.0 breakout boards
<Fritz schematic here>

Currently implemented:
- All electronic components working with watering.py: soil moisture sensor can be successfully read, motor can be flicked on and off, humidity and ambient temperature can be read reliably
- Basic functionality is working overall (if dry then water, else pass) 
- Flask web app interface is able to fetch data from sensors and display them
- Enable/disable auto-watering and force water functionality 

Currently unimplemented:
- GetLastWatered function for reading/writing to a .txt log file
- 

Bugs:
- Humidity/temperature sensor is unable to successfully get both readings on every single call to the Adafruit_DHT.read function. Need to find a workaround -> ignore failed readings, take the average of the most recent 5 successful readings and return the recorded average where needed
