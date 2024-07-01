from flask import Flask, render_template, jsonify
import RPi.GPIO as GPIO
import time

# Sensor pin setup
sensor_pin = 17
humidity_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)

# Function to read sensor data
def read_sensor(pin):
  if GPIO.input(pin) == GPIO.HIGH:
    return "Dry"
  else:
    return "Wet"

# Flask app setup
app = Flask(_IrrigationSystem_)

# Route to display sensor data on a webpage
@app.route("file:///C:/Users/user/FYP%20frontend/dashboard.html")
def dashboard():
  moisture_level = read_sensor(sensor_pin)
  humidity_level = read_sensor(humidity_pin)  # Assuming similar logic for humidity
  return render_template("dashboard.html", moisture=moisture_level, humidity=humidity_level)

# Route to provide data in JSON format (optional)
#@app.route("/api/data")
#def api_data():
 # moisture_level = read_sensor(sensor_pin)
  #humidity_level = read_sensor(humidity_pin)  # Assuming similar logic for humidity
  #data = {"moisture": moisture_level, "humidity": humidity_level}
  #return jsonify(data)

if _name_ == "_main_":
  try:
    app.run(host='0.0.0.0', port=5000)  # Run on all interfaces, port 5000
  except KeyboardInterrupt:
    GPIO.cleanup()