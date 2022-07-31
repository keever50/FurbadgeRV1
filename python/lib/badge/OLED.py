import board
import busio
import digitalio
import time
import microcontroller
import os
import adafruit_ssd1305

# Create the OLED interface.
oled_spi = busio.SPI(board.GP10, board.GP11)
oled_cs = digitalio.DigitalInOut(board.GP9)
oled_dc = digitalio.DigitalInOut(board.GP7)
oled_res = digitalio.DigitalInOut(board.GP6)
oled = adafruit_ssd1305.SSD1305_SPI(128, 32, oled_spi, oled_dc, oled_res, oled_cs)

Booster = digitalio.DigitalInOut(board.GP24)
Booster.direction = digitalio.Direction.OUTPUT  

def Test():
    #OLED TEST#
    #Horizontal lines!
    for Y in range(32):
        for X in range(128):
            oled.pixel(X,Y,Y%2)
    oled.show()
    time.sleep(0.1)
    #Vertical lines!
    for Y in range(32):
        for X in range(128):
            oled.pixel(X,Y,X%2)
    oled.show()
    time.sleep(0.1)
    #Clearing it all!
    for Y in range(32):
        for X in range(128):
            oled.pixel(X,Y,0)
    oled.show()
    #Hoping it passed because i can't see it!

def Power(state):
    if state == True:
        Booster.value = True
        time.sleep(0.1) #To stabilize 
    else:
        oled.fill(1) #To discharge capacitors
        time.sleep(0.2)
        Booster.value = False
        
def show(array):
    for y in range(32):
        for x in range(128):
            p = array[(y*128)+x]
            if p > 0:
                oled.pixel(x,y,0)
            else:
                oled.pixel(x,y,1)
    oled.show()
    
    