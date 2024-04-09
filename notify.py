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
    sleep_time_sec = int(os.getenv('SLEEP_TIME_SEC', 30))
    while True:
        time.sleep(0.1)
        # Skip if no input received
        if not GPIO.input(input_pin):
            continue
        print("Input received from GPIO pin {}".format(input_pin))

        # Send LINE message
        line_message()
        # Sleep to avoid multiple notifications
        time.sleep(sleep_time_sec)

# Send LINE message
def line_message():
    url = "https://api.line.me/v2/bot/message/push"
    access_token = os.getenv('ACCESS_TOKEN')
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    # Loop through user_ids
    user_ids = os.getenv('USER_IDS').split(',')
    for user_id in user_ids:
        payload = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": os.getenv('MESSAGE'),
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        print("Response:", response.text)
        retry_count = 0
        # Retry 3 times if status code is not 200 series
        while retry_count < 3 and not (200 <= response.status_code < 300):
            response = requests.post(url, headers=headers, json=payload)
            print("Failed to send LINE message: " + response.status_code + ", " + response.text)
            print("Retry count: " + str(retry_count))
            retry_count += 1

        if 200 <= response.status_code < 300:
            print("Success to send LINE message")
        else:
            print("Failed to send LINE message: " + response.status_code + ", " + response.text)

main()
