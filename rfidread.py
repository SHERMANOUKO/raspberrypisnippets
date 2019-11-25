import json
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gpiozero import Buzzer
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

buzzer = 17
led = 18
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
reader = SimpleMFRC522()

def buzzer_on():
    """sets buzzer on and off on succesful read"""
	GPIO.output(buzzer,GPIO.HIGH)
	GPIO.output(led,GPIO.HIGH)
	sleep(1)
	GPIO.output(buzzer,GPIO.LOW)
	GPIO.output(led,GPIO.LOW)

while True:
	try:
		id, details= reader.read()
		details = json.loads(details)
		details["tagID"]=id
		buzzer_on()
	except ValueError:
		print("Invalid data format sent")
	except:
		print("Error reading card")
        