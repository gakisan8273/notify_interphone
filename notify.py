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
        if GPIO.input(input_pin):
            print("Input received from GPIO pin {}".format(input_pin))
            line_message()
            time.sleep(30)

# Send LINE push message
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
    print(response.status_code)
    print(response.text)

main()
