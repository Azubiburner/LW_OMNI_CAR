import time
import curses
from rpi_ws281x import PixelStrip, Color
import board
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit

LED_COUNT = 4
LED_PIN = 10
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 155
LED_INVERT = False
LED_CHANNEL = 0

leds = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
leds.begin()

# Motorsteuerung initialisieren
kit = MotorKit(i2c=board.I2C())
kit.motor1.throttle = 0
kit.motor2.throttle = 0
kit.motor3.throttle = 0
kit.motor4.throttle = 0

S = 1.0  # Geschwindigkeit

# Initialisieren der GPIO-Pins für die Motorimpulse
PULSE_M1 = 16
PULSE_M2 = 19
PULSE_M3 = 20
PULSE_M4 = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(PULSE_M1, GPIO.IN)
GPIO.setup(PULSE_M2, GPIO.IN)
GPIO.setup(PULSE_M3, GPIO.IN)
GPIO.setup(PULSE_M4, GPIO.IN)

# Zähler für die Impulse der Motoren
m1 = 0
m2 = 0
m3 = 0
m4 = 0

# Funktion zur Handhabung der Impulse
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

def are_motors_active():
    if kit.motor1.throttle != 0 or kit.motor2.throttle != 0 or kit.motor3.throttle != 0 or kit.motor4.throttle != 0:
        return True
    return False

def blink_leds():
    for i in range(LED_COUNT):
        leds.setPixelColor(i, Color(0, 255, 0))  
    leds.show()
    time.sleep(0.2)  

    for i in range(LED_COUNT):
        leds.setPixelColor(i, Color(0, 0, 0))  
    leds.show()
    time.sleep(0.2)  

def light_on():
    for i in range(LED_COUNT):
        leds.setPixelColor(i, Color(0, 255, 0))  
    leds.show()

def light_off():
    for i in range(LED_COUNT):
        leds.setPixelColor(i, Color(0, 0, 0)) 
    leds.show()