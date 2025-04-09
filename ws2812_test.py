import time
from rpi_ws281x import PixelStrip, Color
LED_COUNT = 4					# Anzahl der LED’s.
LED_PIN = 10             	# GPIO Pin (SPI).
LED_FREQ_HZ = 800000  		# Taktrate der LED’s
LED_DMA = 10          		# DMA Kanal
LED_BRIGHTNESS = 155  		# Helligkeit (0-255)
LED_INVERT = False    		# Signal Invertieren 
LED_CHANNEL = 0       		# PWM Kanal (nicht ändern)
leds = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, 
						LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
leds.begin()
#grün, rot, blau
i=1
while True:
        leds.setPixelColor(i%4, Color(0,255,0))
        leds.setPixelColor((i-1)%4, Color(0,0,0))
        i=i+1
        leds.show()
        time.sleep(0.2)
