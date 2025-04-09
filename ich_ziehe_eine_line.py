import RPi.GPIO as GPIO
import time
import board
from adafruit_motorkit import MotorKit
GPIO.setmode(GPIO.BCM)
SENSOR = 5
GPIO.setup(SENSOR, GPIO.IN)
def zieh_ne_line():
        while (GPIO.input(SENSOR)):
                GPIO.setup(SENSOR, GPIO.IN) 
                kit = MotorKit(i2c=board.I2C())
                kit.motor1.throttle = 0.9
                kit.motor2.throttle = 0.9
                kit.motor3.throttle = 0.9
                kit.motor4.throttle = 0.9 
        else:
                suche_ne_line()   
def suche_ne_line():
        while (GPIO.input(SENSOR))==False:
                suchzeit = 0.5
                GPIO.setup(SENSOR, GPIO.IN)      
                kit = MotorKit(i2c=board.I2C()) 
                kit.motor1.throttle = -0.8
                kit.motor2.throttle = 0.8
                kit.motor3.throttle = -0.8
                kit.motor4.throttle = 0.8
                time.sleep(suchzeit+suchzeit*0.1)
                suchzeit = suchzeit*2
                if suchzeit >= 4:
                        GPIO.setup(SENSOR, GPIO.IN)
                        kit.motor1.throttle = 0.8
                        kit.motor2.throttle = -0.8
                        kit.motor3.throttle = 0.8
                        kit.motor4.throttle = -0.8
                        if (GPIO.input(SENSOR)):
                                zieh_ne_line()
                if (GPIO.input(SENSOR)):
                        kit.motor1.throttle = -0.8
                        kit.motor2.throttle = 0.8
                        kit.motor3.throttle = -0.8
                        kit.motor4.throttle = 0.8
                        time.sleep(0.2)
                        zieh_ne_line()
                  
                if (GPIO.input(SENSOR)):
                        zieh_ne_line()        
                GPIO.setup(SENSOR, GPIO.IN)
                kit.motor1.throttle = 0.8
                kit.motor2.throttle = -0.8
                kit.motor3.throttle = 0.8
                kit.motor4.throttle = -0.8
                time.sleep(suchzeit)
                suchzeit = suchzeit*2
                if suchzeit >= 4:
                        GPIO.setup(SENSOR, GPIO.IN)
                        kit.motor1.throttle = -0.8
                        kit.motor2.throttle = 0.8
                        kit.motor3.throttle = -0.8
                        kit.motor4.throttle = 0.8
                        if (GPIO.input(SENSOR)):
                                zieh_ne_line()  
                if (GPIO.input(SENSOR)):
                        kit.motor1.throttle = 0.8
                        kit.motor2.throttle = -0.8
                        kit.motor3.throttle = 0.8
                        kit.motor4.throttle = -0.8
                        time.sleep(0.2)
                        zieh_ne_line()                     
while True:
        zieh_ne_line()
        