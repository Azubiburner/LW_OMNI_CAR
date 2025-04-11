import lib.LichterWeb as l
import lib.Halt_stop as h
import lib.Labyrinth as lab
from lib.Labyrinth import navigate
import lib.ich_ziehe_eine_line as line
import threading
import lib.movement as m
#import curses as c
import RPi.GPIO as GPIO
import time


#stdscr = c.initscr()
move = 0
event = 0

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

def lights_control():
	while(event == 1):
		if(move != 0):
			l.blink_leds()
			if(move == 1):
				if h.abstand_klein():
					m.stop()
	while(event == 3):
		line.licht_fahrt()
            

def labyrinth():
	try:
		navigate()
	except Exception as error:
		print("An exception occurred:", error)
		m.stop()
		event = 0

def followLine():
	try:
		line.zieh_ne_line()
	except Exception as error:
		print("An exception occurred:", error)
		m.stop()
		event = 0


# Start motor control thread
l.light_off()



async def command_execute(comm,linesearch):
    labsearch = threading.Thread(target=labyrinth)
    searchline = threading.Thread(target=followLine)
    
    print(f"Verarbeite Befehl: {comm}")
    #print("hi"=='hi')
    
    # Hier können Sie den empfangenen Befehl verarbeiten
    commands = ["forward", "backward", "left", "right", "diagonal-left","diagonal-down-left", "diagonal-right", "diagonal-down-right", "stop", "turn-left", "turn-right","findline","lab"]
    if comm in commands:
        print(f"Der Befehl '{comm}' ist gültig.")
        match comm:
            case "forward":
                print("test")
                m.forward()
            case "backward":
                m.backward()
            case "left":
                m.left()
            case "right":
                m.right()
            case "diagonal-left":
                m.diatopleft()
            case "diagonal-down-right":
                m.diadownright()
            case "diagonal-right":
                m.diatopright()
            case "diagonal-down-left":
                m.diadownleft()    
            case "stop":
                lab.t.do_run = False
                line.t.do_run = False
                m.stop()
            case "turn-left":
                m.roleft()
            case "turn-right":
                print("Turn-Right")
                m.roright()
            case "findline":
                print("findline")
                lab.t.do_run = False
                time.sleep(1)
                line.t.do_run = True
               # lab.t.do_run = False
 #                  searchline = threading.Thread(target=followLine, daemon=True)
                searchline.start()
            case "lab":
                print("lab")
                line.t.do_run = False
                time.sleep(1)
                lab.t.do_run = True
                labsearch.start()

            
    else:
        print(f"Der Befehl '{comm}' ist ungültig.")
    return linesearch


"""
async def manualControl(comm):	

	print(f"Verarbeite Befehl: {comm}")
    
    # Hier können Sie den empfangenen Befehl verarbeiten
    befehl = ["forward", "backward", "left", "right", "diagonal-left","diagonal-down-left", "diagonal-right", "diagonal-down-right", "stop", "turn-left", "turn-right","findline","lab"]
	if comm in befehl:
        print(f"Der Befehl '{comm}' ist gültig.")
        match comm:
            case "forward":
                m.forward()
            case "backward":
                m.backward()
            case "left":
                m.left()
            case "right":
                m.right()
            case "diagonal-left":
                m.diatopleft()
            case "diagonal-down-right":
                m.diadownright()
            case "diagonal-right":
                m.diatopright()
            case "diagonal-down-left":
                m.diadownleft()    
            case "stop":
                m.stop()
            case "turn-left":
                m.roleft()
            case "turn-right":
                m.roright()
            case "findline":
            case "lab":

            
    else:
        print(f"Der Befehl '{comm}' ist ungültig.")
	
	try:
		global move
		while True:
			key = stdscr.getkey()
			stdscr.clear()
			if key.lower() == "w":
				m.forward()
				if(move != 1):
					resetCheck()
					move = 1
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
				move = 0
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

			elif key.lower() == "t":
				m.stop()
				event = 0
				break

			if move == 1 or move == 2:
				calcFactor()

			if key.lower() == "l":
				print(f"{m.mfactor1} {m.mfactor2} {m.mfactor3} {m.mfactor4}\n{factors[0]} {factors[1]} {factors[2]} {factors[3]}")
				continue

	except Exception as error:
		print("An exception occurred:", error)
		m.stop()
		event = 0
		print(f"{m.mfactor1} {m.mfactor2} {m.mfactor3} {m.mfactor4}")
		"""



"""
if __name__ == "__main__":
	while(True):
		key = stdscr.getkey()
		stdscr.clear()
		if key.lower() == "1":
			event = 1
			print("Starting Manual Control!")
			manualControl("hallo")

		if key.lower() == "2":
			event = 2
			print("Starting Auto Control for Labyrinth!")
			labyrinth("hallo")

		if key.lower() == "3":
			event = 3
			print("Starting Auto Control for Following a Line!")
			followLine("hallo")
                  """