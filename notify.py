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
        time.sleep(0.1)
        # Skip if no input received
        if not GPIO.input(input_pin):
            continue
        print("Input received from GPIO pin {}".format(input_pin))

        # Send LINE message
        line_message()
        # Sleep for 30 seconds to avoid multiple notifications
        time.sleep(30)

# Send LINE message
def line_message():
    url = "https://api.line.me/v2/bot/message/push"
    access_token = os.getenv('ACCESS_TOKEN')
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    message = "インターホンがなりました"
    # 環境変数のUSER_IDSでループする
    user_ids = os.getenv('USER_IDS').split(',')
    for user_id in user_ids:
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
        print("Response:", response.text)
        retry_count = 0
        # リトライ数が2回まで かつ ステータスコードが200系でない場合はリトライする
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
