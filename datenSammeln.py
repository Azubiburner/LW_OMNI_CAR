import time
import board
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
import logging

logging.basicConfig(filename='motor_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

PULSE_M1 = 16
PULSE_M2 = 19
PULSE_M3 = 20
PULSE_M4 = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(PULSE_M1, GPIO.IN)
GPIO.setup(PULSE_M2, GPIO.IN)
GPIO.setup(PULSE_M3, GPIO.IN)
GPIO.setup(PULSE_M4, GPIO.IN)

m1 = 0
m2 = 0
m3 = 0
m4 = 0

def handler_M1(channel):
    global m1
    m1 += 1

def handler_M2(channel):
    global m2
    m2 += 1

def handler_M3(channel):
    global m3
    m3 += 1

def handler_M4(channel):
    global m4
    m4 += 1

kit = MotorKit(i2c=board.I2C())
S = 1.0

radumfang = 18.54

PDM_M1 = 127
PDM_M2 = 128
PDM_M3 = 130
PDM_M4 = 123

def berechne_strecke(impulse, PDM, radumfang):
    return (impulse / PDM) * radumfang

GPIO.add_event_detect(PULSE_M1, GPIO.FALLING, callback=handler_M1)
GPIO.add_event_detect(PULSE_M2, GPIO.FALLING, callback=handler_M2)
GPIO.add_event_detect(PULSE_M3, GPIO.FALLING, callback=handler_M3)
GPIO.add_event_detect(PULSE_M4, GPIO.FALLING, callback=handler_M4)

def start_fahrt():
    global m1, m2, m3, m4

    """ 
    kit.motor1.throttle = S
    kit.motor2.throttle = S
    kit.motor3.throttle = S
    kit.motor4.throttle = S 
    """

    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        """
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0
        print("Messung gestoppt.")
        """

        strecke_M1 = berechne_strecke(m1, PDM_M1, radumfang)
        strecke_M2 = berechne_strecke(m2, PDM_M2, radumfang)
        strecke_M3 = berechne_strecke(m3, PDM_M3, radumfang)
        strecke_M4 = berechne_strecke(m4, PDM_M4, radumfang)

        gesamt_strecke = (strecke_M1 + strecke_M2 + strecke_M3 + strecke_M4) / 4
        gesamt_strecke_in_meter = gesamt_strecke / 100
        
        log_message = f"Zurückgelegte Strecke: {gesamt_strecke_in_meter:.2f} Meter"
        logging.info(log_message)
        print(log_message)

start_fahrt()
