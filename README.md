# Hydroponix
For automated plant watering systems

Main features:
- 
- 

Currently implemented:
- All hardware components mostly working with watering.py: soil moisture sensor can be successfully read, motor can be flicked on and off, humidity and ambient temperature can be read reliably
- Basic functionality is working overall (if dry then water, else pass) 
- Flask web app interface is able to fetch data from sensors and display them

Currently unimplemented:
- GetLastWatered function for reading/writing to a .txt log file
- Enable/disable watering functionality

Bugs:
- Humidity/temperature sensor is unable to successfully get both readings on every single call to the Adafruit_DHT.read function. Need to find a workaround -> ignore failed readings, take the average of the most recent 5 successful readings and return the recorded average where needed
