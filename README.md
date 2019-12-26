# Hydroponix
For automated plant watering systems

Main features:
- 
- 

Currently implemented:
- Soil moisture sensor can be successfully read and its data 

Currently unimplemented:
- 

Bugs:
- Humidity/temperature sensor is unable to successfully get both readings on every single call to the Adafruit_DHT.read function. Need to find a workaround -> ignore failed readings, take the average of the most recent 5 successful readings and return the recorded average where needed

