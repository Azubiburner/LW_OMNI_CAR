import time
import curses
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 4
LED_PIN = 10
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 155
LED_INVERT = False
LED_CHANNEL = 0

leds = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
leds.begin()

def blink_leds():
    for i in range(LED_COUNT):
        leds.setPixelColor(i, Color(0, 255, 0))  
    leds.show()
    time.sleep(0.2)  

    for i in range(LED_COUNT):
        leds.setPixelColor(i, Color(0, 0, 0))  
    leds.show()
    time.sleep(0.2)  

def light_off():
    for i in range(LED_COUNT):
        leds.setPixelColor(i, Color(0, 0, 0)) 
    leds.show()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(10)

    try:
        while True:
            key = stdscr.getch()

            if key in [ord('w'), ord('a'), ord('s'), ord('d')]:
                while key in [ord('w'), ord('a'), ord('s'), ord('d')]:
                    blink_leds()
                    key = stdscr.getch()
                    while stdscr.getch() != -1:
                        pass
                    time.sleep(0.1)
            else:
                light_off()
                time.sleep(0.01)

    except KeyboardInterrupt:
        light_off()

curses.wrapper(main)
