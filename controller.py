import movement as m
import curses as c
import RPi.GPIO as GPIO

stdscr = c.initscr()
move = 0

PULSE_M1=16;PULSE_M2=19;PULSE_M3=20;PULSE_M4=21
GPIO.setmode(GPIO.BCM)
GPIO.setup(PULSE_M1, GPIO.IN)
GPIO.setup(PULSE_M2, GPIO.IN)
GPIO.setup(PULSE_M3, GPIO.IN)
GPIO.setup(PULSE_M4, GPIO.IN)

factors = [1.0, 1.0, 1.0, 1.0]

def handler_M1(channel): factors[0];factors[0]=factors[0]+1
def handler_M2(channel): factors[1];factors[1]=factors[1]+1
def handler_M3(channel): factors[2];factors[2]=factors[2]+1
def handler_M4(channel): factors[3];factors[3]=factors[3]+1

GPIO.add_event_detect(PULSE_M1, GPIO.FALLING,callback=handler_M1)
GPIO.add_event_detect(PULSE_M2, GPIO.FALLING,callback=handler_M2)
GPIO.add_event_detect(PULSE_M3, GPIO.FALLING,callback=handler_M3)
GPIO.add_event_detect(PULSE_M4, GPIO.FALLING,callback=handler_M4)

def resetCheck():
	factors[0] = 1.0
	factors[1] = 1.0
	factors[2] = 1.0
	factors[3] = 1.0

def calcFactor():
	m.mfactor1 = min(factors) / factors[0]
	m.mfactor2 = min(factors) / factors[1]
	m.mfactor3 = min(factors) / factors[2]
	m.mfactor4 = min(factors) / factors[3]
	m.update(move)

try:
	while True:
		key = stdscr.getkey()
		stdscr.clear()
		if key.lower() == "w":
			m.forward()
			if(move != 1):
				resetCheck()
				move = 1
			calcFactor()
			continue

		elif key.lower() == "a":
			m.left()
			if(move != 4):
				resetCheck()
				move = 4
			continue

		elif key.lower() == "s":
			m.backward()
			if(move != 2):
				resetCheck()
				move = 2
			calcFactor()
			continue

		elif key.lower() == "d":
			m.right()
			if(move != 3):
				resetCheck()
				move = 3
			continue

		elif key.lower() == "r":
			m.stop()
			resetCheck()
			continue

		elif key.lower() == "q":
			m.roleft()
			move = 6
			resetCheck()
			continue

		elif key.lower() == "e":
			m.roright()
			move = 5
			resetCheck()
			continue

		elif key.lower() == "-" and not m.s < 0.82:
			m.s -= 0.02
			m.update(move)
			resetCheck()
			continue

		elif key.lower() == "+" and not m.s > 0.98:
			m.s += 0.02
			m.update(move)
			resetCheck()
			continue

		elif key.lower() == "#":
			if(m.s != 1.0):
				m.s = 1.0
			else:
				m.s = 0.8
			m.update(move)
			resetCheck()
			continue

		if move == 1 or move == 2:
			calcFactor()

		if key.lower() == "l":
			print(f"{m.mfactor1} {m.mfactor2} {m.mfactor3} {m.mfactor4}\n{factors[0]} {factors[1]} {factors[2]} {factors[3]}")
			continue

except Exception as error:
	print("An exception occurred:", error)
	m.stop()
	print(f"{m.mfactor1} {m.mfactor2} {m.mfactor3} {m.mfactor4}")
