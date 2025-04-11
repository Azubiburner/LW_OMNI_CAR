# import RPi.GPIO as GPIO
import time
# import board
import threading
# from adafruit_motorkit import MotorKit
# from rpi_ws281x import PixelStrip, Color

# GPIO.setmode(GPIO.BCM)
SENSOR = 5

# LED_COUNT = 4
# LED_PIN = 10
# LED_FREQ_HZ = 800000
# LED_DMA = 10
# LED_BRIGHTNESS = 155
# LED_INVERT = False
# LED_CHANNEL = 0

# leds = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# leds.begin()
# GPIO.setup(SENSOR, GPIO.IN)
t = threading.currentThread() 

def test():
        while getattr(t, "do_run",True):
                print("ich suche eine line")

def zieh_ne_line():
        while (getattr(t, "do_run",True) and GPIO.input(SENSOR)):
                # GPIO.setup(SENSOR, GPIO.IN) 
                # kit = MotorKit(i2c=board.I2C())
                # kit.motor1.throttle = 0.9
                # kit.motor2.throttle = 0.9
                # kit.motor3.throttle = 0.9
                # kit.motor4.throttle = 0.9 
                pass
        else:
                suche_ne_line() 

def suche_ne_line():
        while (getattr(t, "do_run",True) and GPIO.input(SENSOR))==False:
                suchzeit = 0.5
                # GPIO.setup(SENSOR, GPIO.IN)      
                # kit = MotorKit(i2c=board.I2C()) 
                # kit.motor1.throttle = -0.8
                # kit.motor2.throttle = 0.8
                # kit.motor3.throttle = -0.8
                # kit.motor4.throttle = 0.8
                time.sleep(suchzeit)
                suchzeit = suchzeit*2
                if suchzeit >= 6:
                        # GPIO.setup(SENSOR, GPIO.IN)
                        # kit.motor1.throttle = 0.8
                        # kit.motor2.throttle = -0.8
                        # kit.motor3.throttle = 0.8
                        # kit.motor4.throttle = -0.8
                        if (GPIO.input(SENSOR)):
                                zieh_ne_line()
                if (GPIO.input(SENSOR)):
                        # kit.motor1.throttle = -0.8
                        # kit.motor2.throttle = 0.8
                        # kit.motor3.throttle = -0.8
                        # kit.motor4.throttle = 0.8
                        time.sleep(0.1)
                        zieh_ne_line()
                
                if (GPIO.input(SENSOR)):
                        zieh_ne_line()        
                # GPIO.setup(SENSOR, GPIO.IN)
                # kit.motor1.throttle = 0.8
                # kit.motor2.throttle = -0.8
                # kit.motor3.throttle = 0.8
                # kit.motor4.throttle = -0.8
                time.sleep(suchzeit)
                suchzeit = suchzeit*2
                if suchzeit >= 6:
                        # GPIO.setup(SENSOR, GPIO.IN)
                        # kit.motor1.throttle = -0.8
                        # kit.motor2.throttle = 0.8
                        # kit.motor3.throttle = -0.8
                        # kit.motor4.throttle = 0.8
                        if (GPIO.input(SENSOR)):
                                zieh_ne_line()  
                if (GPIO.input(SENSOR)):
                        # kit.motor1.throttle = 0.8
                        # kit.motor2.throttle = -0.8
                        # kit.motor3.throttle = 0.8
                        # kit.motor4.throttle = -0.8
                        time.sleep(0.1)
                        zieh_ne_line()                     

def licht_fahrt():
        # global leds
        while (GPIO.input(SENSOR)):
                # for i in range(LED_COUNT): 
                #         leds.setPixelColor(i, Color(0, 0, 255)) 
                # leds.show()
                time.sleep(0.2)
        else:
                # for i in range(LED_COUNT):
                #         leds.setPixelColor(i, Color(0, 255, 0))  
                # leds.show()
                time.sleep(0.2)
                # for i in range(LED_COUNT):
                #         leds.setPixelColor(i, Color(0, 0, 255))
                # leds.show()
                time.sleep(0.2) 
                licht_fahrt()

if __name__ == "__main__":
        licht_thread = threading.Thread(target=licht_fahrt,daemon=False)
        licht_thread.start()
        while True:
                zieh_ne_line()

