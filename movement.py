import time
import board
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c = board.I2C())
s = 1.0

mfactor1 = 0.8
mfactor2 = 0.8
mfactor3 = 0.8
mfactor4 = 0.8

def calcThrottle(mfactor:float):
	if(mfactor <= 1 and mfactor >= 0.8):
		return ((1 - mfactor) * 5)
	return 0.0

def forward()-> None:
	kit.motor1.throttle = s - calcThrottle(mfactor1)
	kit.motor2.throttle = s - calcThrottle(mfactor2)
	kit.motor3.throttle = s - calcThrottle(mfactor3)
	kit.motor4.throttle = s - calcThrottle(mfactor4)

def backward()-> None:
	kit.motor1.throttle = -s + calcThrottle(mfactor1)
	kit.motor2.throttle = -s + calcThrottle(mfactor2)
	kit.motor3.throttle = -s + calcThrottle(mfactor3)
	kit.motor4.throttle = -s + calcThrottle(mfactor4)

def stop()-> None:
	kit.motor1.throttle = 0
	kit.motor2.throttle = 0 
	kit.motor3.throttle = 0 
	kit.motor4.throttle = 0

def right()-> None:
	kit.motor1.throttle = s
	kit.motor2.throttle = -s
	kit.motor3.throttle = -s
	kit.motor4.throttle = s

def left()-> None:
	kit.motor1.throttle = -s
	kit.motor2.throttle = s
	kit.motor3.throttle = s
	kit.motor4.throttle = -s

def roright()-> None:
	kit.motor1.throttle = -s
	kit.motor2.throttle = s
	kit.motor3.throttle = -s
	kit.motor4.throttle = s

def roleft()-> None:
	kit.motor1.throttle = s
	kit.motor2.throttle = -s
	kit.motor3.throttle = s
	kit.motor4.throttle = -s

def diatopleft()-> None:
	kit.motor1.throttle = 0
	kit.motor2.throttle = s 
	kit.motor3.throttle = s
	kit.motor4.throttle = 0

def diadownright()-> None:
	kit.motor1.throttle = 0
	kit.motor2.throttle = -s
	kit.motor3.throttle = -s
	kit.motor4.throttle = 0

def diatopright() -> None:
	kit.motor1.throttle = s
	kit.motor2.throttle = 0 
	kit.motor3.throttle = 0 
	kit.motor4.throttle = s

def diadownleft() -> None:
	kit.motor1.throttle = -s
	kit.motor2.throttle = 0 
	kit.motor3.throttle = 0 
	kit.motor4.throttle = -s

def update(move:int) -> None:
	match move:
		case 0:
			stop()
		case 1:
			forward()
		case 2:
			backward()
		case 3:
			right()
		case 4:
			left()
		case 5:
			roright()
		case 6:
			roleft()
		case 7:
			diatopright()
		case 8:
			diadownright()
		case 9:
			diatopleft()
		case 10:
			diadownleft()


