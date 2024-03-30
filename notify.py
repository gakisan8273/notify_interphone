import time
import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin
input_pin = 17
GPIO.setup(input_pin, GPIO.IN)

# Main loop
def main():
    while True:
        time.sleep(0.5)
        # Skip if no input received
        if not GPIO.input(input_pin):
            continue
        print("Input received from GPIO pin {}".format(input_pin))

        # Send LINE message
        response = line_message()
        # Sleep for 30 seconds if succeeded to send LINE message
        if 200 <= response.status_code < 300:
            time.sleep(30)
        else:
            # Retry soon if failed to send LINE message
            print("Failed to send LINE message: " + response.text)

# Send LINE message
def line_message():
    url = "https://api.line.me/v2/bot/message/push"
    access_token = os.getenv('ACCESS_TOKEN')
    user_id = os.getenv('USER_ID')
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    message = "インターホンがなりました"
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message,
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response

main()
