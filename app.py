from flask import Flask, render_template, redirect, url_for
import datetime
import watering
import calendar
import psutil
import os
import logging
import sys
import main

app = Flask(__name__)

# ===== Configuration =====
logging.basicConfig(level=logging.INFO)

# ===== Helper Functions =====
# Function to append "st", "nd", "rd", "th" to any day of the month 
def ord(n):
    tail = ""
    if n % 100 >= 4 and n % 100 <= 20:
        tail = "th"
    else:
        # If the result of n % 10 is not 1, 2 or 3, then the tail defaults to "th" 
        tail = {1:"st", 2:"nd", 3:"rd"}.get(n % 10, "th")
    return str(n) + tail

# Forms a dictionary of data to write into the main HTML file
def GetTemplateData(title = "Hydroponix"):
    currTime = datetime.datetime.now()
    timeString = "{0} {1}, {2}".format(ord(currTime.day), calendar.month_name[currTime.month], currTime.year)
    humidAndTempData = main.GetHumidityAndTemp();
    humidity = "{0}%".format(round(humidAndTempData["humidity"]))
    temperature = "{0}°C".format(humidAndTempData["temperature"])	
    return {
        'title' : title,
        'time' : timeString,
        'humidity' : humidity,
        'temperature' : temperature  
    }

def IsProcessActive():
    for process in psutil.process_iter():
        try:
            if process.cmdline()[1] == "watering.py":
                return True
        except:
            pass
    return False

# ===== Routes =====
# Displays the homepage
@app.route("/")
def Main():
    templateData = GetTemplateData()  # Calls GetLastWatered which returns a string containing the last time automatic watering occurred. Sets this as 
    return render_template("index.html", **templateData)

@app.route("/water_once")
def WaterOnce():
    templateData = GetTemplateData()
    logging.info("Watering once!")
    # TODO: Let the user set the force water interval in the front end
    watering.ForceWater(1)
    return render_template("index.html", **templateData)

@app.route("/auto_watering/ON")
def AutoWaterOn():
    logging.info("Auto watering on")
    templateData = GetTemplateData()
    if not IsProcessActive():
        logging.info("STARTING the watering process NOW")
        os.system("python3 watering.py &")
    else:
        logging.info("Process is ALREADY RUNNING")
    return render_template("index.html", **templateData)

@app.route("/auto_watering/OFF")
def AutoWaterOff():
    logging.info("Auto watering off")
    templateData = GetTemplateData()
    watering.ResetState()
    if not IsProcessActive():
        logging.info("Process is ALREADY OFF")
    else:
        logging.info("STOPPING the process NOW")
        os.system("pkill -f watering.py")
    return render_template("index.html", **templateData)

if __name__ == "__main__":
    watering.ResetState()
    logging.info("Starting main")
    app.run(host='0.0.0.0', port=int(sys.argv[1]), debug=True)

