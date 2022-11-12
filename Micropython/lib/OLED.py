import time
import os
from machine import SPI, Pin
from lib import ssd1305

# Create the OLED interface.

# Select hardware SPI 1 (SCK = GPIO10, MOSI = GPIO11)
oled_spi = SPI(1)
oled_cs = Pin(9, Pin.OUT)
oled_dc = Pin(7, Pin.OUT)
oled_res = Pin(6, Pin.OUT)
driver = ssd1305.SSD1305_SPI(128, 32, oled_spi, oled_dc, oled_res, oled_cs)

booster = Pin(24, Pin.OUT)

def power_on():
    booster.on()

    # Stabalize
    time.sleep(0.1)

def power_off():
    # Discharge capacitors
    driver.fill(1)
    time.sleep(0.2)

    booster.off()

def test():
    #OLED TEST#
    #Horizontal lines!
    for Y in range(32):
        for X in range(128):
            driver.pixel(X,Y,Y%2)
    driver.show()
    #Vertical lines!
    for Y in range(32):
        for X in range(128):
            driver.pixel(X,Y,X%2)
    driver.show()
    #Clearing it all!
    for Y in range(32):
        for X in range(128):
            driver.pixel(X,Y,0)
    driver.show()
    #Hoping it passed because i can't see it!

def oldshow_image(array):
    for y in range(32):
        for x in range(128):
            p = array[(y*128)+x]
            if p == True:
                driver.pixelf(x,y,False)
            else:
                driver.pixelf(x,y,True)
    driver.show()

def show_image(array):

    for Y in range(32):
        ystride = (Y >> 3) * 128
        offset = Y & 0x07
        T = ~(0x01 << offset)
        for X in range(128):
            color = array[(Y*128)+X]
            index = ystride + X
            driver.buf[index] = ( driver.buf[index] & T ) | ( color << offset )
    driver.show()

#Handling quick frames
frame_list = []

def store_frame(array, ID):
    #create new frame
    frame = bytearray((32 // 8) * 128)

    for Y in range(32):
        ystride = (Y >> 3) * 128
        offset = Y & 0x07
        T = ~(0x01 << offset)
        for X in range(128):
            color = array[(Y*128)+X]
            index = ystride + X
            frame[index] = ( frame[index] & T ) | ( color << offset )
    frame_list.append(frame) ##CHANGE THIS TO ID OR RETURN ID##

def show_frame(ID):
    """Update the display"""

    driver.dc_pin.value = 0
    with driver.spi_device as spi:
        spi.write(bytearray(0x21))
        spi.write(bytearray(4))
        spi.write(bytearray(127 + 4))
        spi.write(bytearray(0x22))
        spi.write(bytearray(0))
        spi.write(bytearray(3))
        driver.dc_pin.value = 1
        spi.write(frame_list[ID])



def bench():
    power_on()

    #OLED TEST#
    time.sleep(1)
    #FILL TEST
    timefirst = time.ticks_ms()

    #index = (y >> 3) * self.stride + x
    #offset = y & 0x07

    ##Extremely fast pixel write##
    Color = True
    for Y in range(32):
        ystride = (Y >> 3) * 128
        offset = Y & 0x07
        T = ~(0x01 << offset)
        for X in range(128):
            index = ystride + X
            driver.buffer[index] = ( driver.buffer[index] & T ) | ( Color << offset )
    driver.show()

    delay = time.ticks_ms() - timefirst
    print("Screenfill delay in ms")
    print(delay*1000)


    ##

    #Clearing it all!
    driver.fill(0)
    driver.show()
