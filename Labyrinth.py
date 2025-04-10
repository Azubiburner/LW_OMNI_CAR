import RPi.GPIO as GPIO
import time
import board
import threading
from adafruit_motorkit import MotorKit
from rpi_ws281x import PixelStrip, Color
GPIO.setmode(GPIO.BCM)
SENSOR = 5

LED_COUNT = 4
LED_PIN = 10
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 155
LED_INVERT = False
LED_CHANNEL = 0

leds = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
leds.begin()

kit = MotorKit(i2c=None)

# Ultrasonic Sensor Setup
TRIGGER = 12
ECHO = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Distance Measurement
def measure_distance():
    GPIO.output(TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)

    start = time.time()
    stop = time.time()

    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()

    return ((stop - start) * 34300) / 2

# Motor Control
def start_motors():
    kit.motor1.throttle = 1.0
    kit.motor2.throttle = 1.0
    kit.motor3.throttle = 1.0
    kit.motor4.throttle = 1.0
    print("Moving forward...")

def stop_motors():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0
    print("Stopped")

def turn_right():
    print("Turning right")
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = 1.0
    kit.motor3.throttle = -1.0
    kit.motor4.throttle = 1.0
    time.sleep(0.7)  # Halbe Zeit für ~45° Drehung
    stop_motors()
    time.sleep(0.5)
    
    # Zweite Drehung für weitere 45°
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = 1.0
    kit.motor3.throttle = -1.0
    kit.motor4.throttle = 1.0
    time.sleep(0.7)  # Halbe Zeit für ~45° Drehung
    stop_motors()
    time.sleep(0.5)

def turn_left():
    print("Turning left")
    kit.motor1.throttle = 1.0
    kit.motor2.throttle = -1.0
    kit.motor3.throttle = 1.0
    kit.motor4.throttle = -1.0
    time.sleep(0.725)  # Halbe Zeit für ~45° Drehung
    stop_motors()
    time.sleep(0.5)
    
    # Zweite Drehung für weitere 45°
    kit.motor1.throttle = 1.0
    kit.motor2.throttle = -1.0
    kit.motor3.throttle = 1.0
    kit.motor4.throttle = -1.0
    time.sleep(0.725)  # Halbe Zeit für ~45° Drehung
    stop_motors()
    time.sleep(0.5)

def turn_around():
    print("Turning around (180°)")
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = 1.0
    kit.motor3.throttle = -1.0
    kit.motor4.throttle = 1.0
    time.sleep(1.425)  # Halbe Zeit für ~90° Drehung
    stop_motors()
    time.sleep(0.5)
    
    # Zweite Drehung für weitere 90°
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = 1.0
    kit.motor3.throttle = -1.0
    kit.motor4.throttle = 1.0
    time.sleep(1.425)  # Halbe Zeit für ~90° Drehung
    stop_motors()
    time.sleep(0.5)

def licht_fahrt():
        global leds
        while (kit.motor1.throttle != 0 and kit.motor2.throttle != 0 and kit.motor3.throttle != 0 and kit.motor4.throttle != 0):
                for i in range(LED_COUNT):
                        leds.setPixelColor(i, Color(0, 255, 0))   
                leds.show()
                time.sleep(0.2)
                for i in range(LED_COUNT):
                        leds.setPixelColor(i, Color(0, 0, 255))   
                leds.show()
                time.sleep(0.2) 
                licht_fahrt()


licht_thread = threading.Thread(target=licht_fahrt,daemon=True)
licht_thread.start()

# Main navigation loop
def navigate():
    try:
        while True:
            front_distance = measure_distance()
            print(f"Front distance: {front_distance:.1f} cm")

            if front_distance < 10.0:
                print("Obstacle ahead! Stopping and scanning sides...")
                stop_motors()

                # Turn to scan right
                turn_right()
                right_distance = measure_distance()
                print(f"Right distance: {right_distance:.1f} cm")

                # Back to center
                turn_left()

                # Turn to scan left
                turn_left()
                left_distance = measure_distance()
                print(f"Left distance: {left_distance:.1f} cm")

                # Back to center
                turn_right()

                # Decision
                if left_distance >= 10.0 and left_distance > right_distance:
                    print("Choosing left path")
                    turn_left()
                elif right_distance >= 10.0:
                    print("Choosing right path")
                    turn_right()
                elif front_distance >= 10.0:
                    print("Front became clear again")
                else:
                    print("Dead end! Turning around.")
                    turn_around()

                # Move forward again
                start_motors()

            else:
                # Path is clear
                start_motors()

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Interrupted by user. Stopping.")
        stop_motors()
        GPIO.cleanup()

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    navigate()
