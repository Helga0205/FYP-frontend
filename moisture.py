3import socket
from tkinter import *
import RPi.GPIO as GPIO
import time

sensor_pin = 17
pump_pin = 18
valve_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.setup(valve_pin, GPIO.OUT)

    #Function to convert and switch on water pump.
def read_moisture():
    if GPIO.input(sensor_pin) == GPIO.HIGH:
       
        GPIO.output(pump_pin, GPIO.HIGH)
        GPIO.output(valve_pin, GPIO.HIGH)
        return "Soil dry switch ON water pump now"
    else:
        GPIO.output(pump_pin, GPIO.LOW)
        GPIO.output(valve_pin, GPIO.LOW)
        return "Soil is Wet switch OFF water pump now"

#creating virtual server for raspberry pi control room.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(1)
print("Server is waiting for incoming connections...")

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('172.20.20.6', 12345))  # Based on the network where raspberry pi IP address

 
    #creating framework window
    root = Tk()
    root.title("Moisture level Display:")
            
  #creating a lebel to display moisture level
            
    label = Label(root, text="Moisture level: ")
    label.pack()
    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from {10.122.80.24} established.")# client ip address

        data = client_socket.recv(1024)
        moisture_level = data.decode()
        label.config(text=("Moisture level: {moisture_level}"))
        print("Received moisture Status: {moisture_level}")

        try:
            while True:
                moisture = read_moisture()
                print(f"Moisture Status: {moisture}")
                time.sleep(5)
        except KeyboardInterrupt:
            client_socket.close()
            
        
        # creating button for receiving and updating the labels
        update_button = Button(root, text ="Update", command=update_label)
        update_button.pack()
        
        root.mainloop()

except KeyboardInterrupt:
    server_socket.close()
    GPIO.cleanup()


#result1 ="<result1>{}</result1>".format(str(GPIO.input(sensor_pin)))
#print(result1)
    
# <result1>75</result1>