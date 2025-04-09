import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIGGER = 12
ECHO = 6
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
counter = 0
def measure():
    GPIO.output(TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)
    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()
    return ((stop-start) * 34300) / 2
'''
while counter < 50:
    print ("%.1f cm" % messure())
    time.sleep(1) 
    distanz= messure()
    counter += 1
    if distanz < 5:
      print ("Weg da du Huhrensohn")
'''
def abstand_klein():
	if measure() < 5:
		return True
	else:
		return False

