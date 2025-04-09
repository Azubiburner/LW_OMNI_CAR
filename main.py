import Halt_stop as hs
import board
from adafruit_motorkit import MotorKit

def main():
  kit = MotorKit(i2c=board.I2C())
	while True:
	  hs.time.sleep(0.2)
	  if hs.abstand_klein():
		print('aus dem Weg Kinder!')
                kit.motor1.throttle = 0.0
                kit.motor2.throttle = 0.0
                kit.motor3.throttle = 0.0
                kit.motor4.throttle = 0.0

	  else
                kit.motor1.throttle = 1.0
                kit.motor2.throttle = 1.0
                kit.motor3.throttle = 1.0
                kit.motor4.throttle = 1.0


if __name__ == '__main__':
	main()
