import json
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
GPIO.setwarnings(False)

while True:
	print("\n\nPress CTRL+Z to exit")
	try:
		name = input("Enter your name")
		details = {
            "name":name
        }

		details = json.dumps(details)
		print("Now place your tag to write")
		reader.write(details)
		print("Written")
	finally:
		GPIO.cleanup()

        