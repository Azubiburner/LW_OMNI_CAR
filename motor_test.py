import time
import board
from adafruit_motorkit import MotorKit
kit = MotorKit(i2c=board.I2C())
kit.motor1.throttle = 1.0
kit.motor2.throttle = 1.0
kit.motor3.throttle = 1.0
kit.motor4.throttle = 1.0
time.sleep(20)
kit.motor2.throttle=-1.0
kit.motor1.throttle=-1.0
kit.motor3.throttle=-1.0
kit.motor4.throttle=-1.0
time.sleep(20)
kit.motor2.throttle=0.0
kit.motor1.throttle=0.0
kit.motor3.throttle=0.0
kit.motor4.throttle=0.0

