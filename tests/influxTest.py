import time
import datetime
import sys
from influxdb import InfluxDBClient


samplingPeriod = 5
timestamp = int(time.time())
print("Timestamp: {}".format(timestamp))
jsonSensorBody = [
    {
        "measurement": "temperature_and_humidity",  # This is the table name
        "tags": {
            "temperature": "25.6",   # These are the columns
            "humidity": "70"
        },
        "fields": {
            "value": 100
        }
    }
]

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'hydroponix')

# client.write_points(jsonSensorBody, time_precision='ms')

result = client.query('select * from temperature_and_humidity;')

print("Result: {0}".format(result))
print(type(result))

dataPoints = list(result.get_points(measurement="temperature_and_humidity"))
print(dataPoints)

print(dataPoints[0])

