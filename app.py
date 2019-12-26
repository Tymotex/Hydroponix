from flask import Flask, render_template, redirect, url_for
import datetime
import watering
import calendar

# Using constructor to create a new flask object
app = Flask(__name__)

# Forms a dictionary of data to write into the main HTML file
def template(title = "Hydroponix"):
	currTime = datetime.datetime.now()
	timeString = str(ord(currTime.day)) + " " + calendar.month_name[currTime.month] + ", " + str(currTime.year)
	lastWatered = watering.GetLastWatered()	
	humidAndTempData = watering.GetHumidityAndTemp();
	humidity = str(round(humidAndTempData["humidity"])) + "%"
	temperature = str(humidAndTempData["temperature"]) + "°C"	
	templateDate = {
		'title' : title,
		'time' : timeString,
		'lastWatering' : lastWatered,
		'humidity' : humidity,
		'temperature' : temperature  
	}
	return templateDate

# Function to append "st", "nd", "rd", "th" to any day of the month 
def ord(n):
	tail = ""
	if n % 100 >= 4 and n % 100 <= 20:
		tail = "th"
	else:
		# If the result of n % 10 is not 1, 2 or 3, then the tail defaults to "th" 
		tail = {1:"st", 2:"nd", 3:"rd"}.get(n % 10, "th")
	return str(n) + tail

# Displays the homepage
@app.route("/")
def main():
	templateData = template()  # Calls GetLastWatered which returns a string containing the last time automatic watering occurred. Sets this as 
	return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
