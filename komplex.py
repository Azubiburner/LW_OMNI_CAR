import time
import board
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from rpi_ws281x import PixelStrip, Color
from threading import Thread
PULSE_M1=16;PULSE_M2=19;PULSE_M3=20;PULSE_M4=21
GPIO.setmode(GPIO.BCM)
GPIO.setup(PULSE_M1, GPIO.IN)
GPIO.setup(PULSE_M2, GPIO.IN)
GPIO.setup(PULSE_M3, GPIO.IN)
GPIO.setup(PULSE_M4, GPIO.IN)
m1=0;m2=0;m3=0;m4=0
def handler_M1(channel): global m1;m1=m1+1
def handler_M2(channel): global m2;m2=m2+1
def handler_M3(channel): global m3;m3=m3+1
def handler_M4(channel): global m4;m4=m4+1
leds = PixelStrip(4,10,800000,10,False,32,0)
leds.begin()
run=True 
def blink(l): 
    i=1
    while(run):
        l.setPixelColor(i%4, Color(0,255,0))
        l.setPixelColor((i-1)%4, Color(0,0,0))
        i=i+1;l.show();time.sleep(0.2) 
Thread(target=blink, args=(leds,)).start()
GPIO.add_event_detect(PULSE_M1, GPIO.FALLING,callback=handler_M1)
GPIO.add_event_detect(PULSE_M2, GPIO.FALLING,callback=handler_M2)
GPIO.add_event_detect(PULSE_M3, GPIO.FALLING,callback=handler_M3)
GPIO.add_event_detect(PULSE_M4, GPIO.FALLING,callback=handler_M4)
kit = MotorKit(i2c=board.I2C())
S=1.0
PDM=63
kit.motor1.throttle=S;kit.motor2.throttle=S;kit.motor3.throttle=S;kit.motor4.throttle=S
m1=0
while(m1<PDM*2): pass
kit.motor1.throttle=S;kit.motor2.throttle=-S;kit.motor3.throttle=-S;kit.motor4.throttle=S
m1=0
while(m1<PDM*2): pass
kit.motor1.throttle=-S;kit.motor2.throttle=-S;kit.motor3.throttle=-S;kit.motor4.throttle=-S
m1=0
while(m1<PDM*2): pass
kit.motor1.throttle=-S;kit.motor2.throttle=S;kit.motor3.throttle=S;kit.motor4.throttle=-S
m1=0
while(m1<PDM*2): pass
kit.motor1.throttle=0;kit.motor2.throttle=0;kit.motor3.throttle=0;kit.motor4.throttle=0
run=False
