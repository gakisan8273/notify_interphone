import time

import RPi.GPIO as GPIO

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin
input_pin = 17
GPIO.setup(input_pin, GPIO.IN)

# Main loop
while True:
    time.sleep(0.5)
    if GPIO.input(input_pin):
        print("Input received from GPIO pin {}".format(input_pin))