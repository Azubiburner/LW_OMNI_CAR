import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
SENSOR = 5
GPIO.setup(SENSOR, GPIO.IN)
while True:
        print(not(GPIO.input(SENSOR)))
        time.sleep(0.2)
