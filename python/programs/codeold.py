# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Import all board pins.
import board
import busio
import digitalio
import time
import microcontroller
import os
# Import the SSD1305 module.
import adafruit_ssd1305
# Define the Reset Pin


#turn on 12V boost
Booster = digitalio.DigitalInOut(board.GP24)
Booster.direction = digitalio.Direction.OUTPUT
Booster.value = True

# Create the I2C interface.
spi = busio.SPI(board.GP10, board.GP11)
cs = digitalio.DigitalInOut(board.GP9)
dc = digitalio.DigitalInOut(board.GP7)
res = digitalio.DigitalInOut(board.GP6)

# Create the SSD1305 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!

display = adafruit_ssd1305.SSD1305_SPI(128, 32, spi, dc, res, cs)

# Alternatively you can change the I2C address of the device with an addr parameter:
# display = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c, addr=0x31, reset=oled_reset)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!

def showImage(path):
    display.fill(0)
    file = open(path, "rb")
    image = file.read()

    b=16402
    for Y in range(32):
        for X in range(128):
            b=b-4
            pix = 255-image[b]
            if pix > 128:
                display.pixel(127-X, Y, pix)
    display.show()    

while True:
    dirs = os.listdir("images")
    for file in dirs:
        print(file)
        showImage("images/"+file)
        microcontroller.delay_us(3000000)
    

#for B in range(4096):
    #display.fill_rect(B%32, round(4096/(B+1)), 1, 1, round(image[B]/255))        
    #display.show()



    #microcontroller.delay_us(1)
    
    #display.fill_rect(i*8,0, (i*8)+8,8, 0)
    
    
