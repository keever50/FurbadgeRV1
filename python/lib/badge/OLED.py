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
driver = adafruit_ssd1305.SSD1305_SPI(128, 32, oled_spi, oled_dc, oled_res, oled_cs)

Booster = digitalio.DigitalInOut(board.GP24)
Booster.direction = digitalio.Direction.OUTPUT  

def Test():
    #OLED TEST#
    #Horizontal lines!
    for Y in range(32):
        for X in range(128):
            driver.pixelf(X,Y,Y%2)
    driver.show()
    #Vertical lines!
    for Y in range(32):
        for X in range(128):
            driver.pixelf(X,Y,X%2)
    driver.show()
    #Clearing it all!
    for Y in range(32):
        for X in range(128):
            driver.pixelf(X,Y,0)
    driver.show()
    #Hoping it passed because i can't see it!

def Power(state):
    if state == True:
        Booster.value = True
        time.sleep(0.1) #To stabilize 
    else:
        driver.fill(1) #To discharge capacitors
        time.sleep(0.2)
        Booster.value = False
        
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
    oled_spi.try_lock()
    oled_spi.configure(baudrate=8000000)
    oled_spi.unlock()
    print("SPI frequency")
    print(oled_spi.frequency)
    
    Power(True)
    
    #OLED TEST#
    time.sleep(1)
    #FILL TEST
    timefirst = time.monotonic()

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
            driver.buf[index] = ( driver.buf[index] & T ) | ( Color << offset ) 
    driver.show()

    delay = time.monotonic() - timefirst        
    print("Screenfill delay in ms")
    print(delay*1000)    
    
    
    ##
    
    #Clearing it all!
    driver.fill(0)
    driver.show()
    
        
    
#bench()

