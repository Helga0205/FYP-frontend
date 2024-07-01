import sqlite3
import socket
from tkinter import *
import RPi.GPIO as GPIO
import time

sensor_pin = 17
pump_pin = 18
valve_pin = 23

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.setup(valve_pin, GPIO.OUT)

# Initialize SQLite database
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_readings
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  moisture_level INTEGER,
                  pump_status TEXT)''')
conn.commit()

# Function to read moisture level and control pump
def read_moisture():
    if GPIO.input(sensor_pin) == GPIO.HIGH:
        GPIO.output(pump_pin, GPIO.HIGH)
        GPIO.output(valve_pin, GPIO.HIGH)
        pump_status = "ON"
        moisture_level = 1  # Example value for dry soil
    else:
        GPIO.output(pump_pin, GPIO.LOW)
        GPIO.output(valve_pin, GPIO.LOW)
        pump_status = "OFF"
        moisture_level = 0  # Example value for wet soil
    
    # Insert sensor readings into the database
    cursor.execute("INSERT INTO sensor_readings (moisture_level, pump_status) VALUES (?, ?)", (moisture_level, pump_status))
    conn.commit()

    return moisture_level, pump_status

# Main function to run the program
def main():
    try:
        while True:
            moisture_level, pump_status = read_moisture()
            print(f"Moisture Level: {moisture_level}, Pump Status: {pump_status}")
            time.sleep(5)  # Adjust the interval as needed

    except KeyboardInterrupt:
        conn.close()
        GPIO.cleanup()

if _name_ == "_main_":
    main()