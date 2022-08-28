#Importing
import board
import busio
import digitalio
import time
import microcontroller
import os
import analogio

##INIT##
import badge
from badge import BMP

#Battery check
BATV_PIN = analogio.AnalogIn(board.GP26)
BATV = (BATV_PIN.value*6.6) / 65536
print("Battery voltage check: BATV = {:5.2f}V".format(BATV) )

if BATV >= 3:
    print("Battery OK. Turning on OLED circuit")
    print("[OLED]Powering on")
    badge.OLED.Power(True)
    print("[OLED]Testing")
    badge.OLED.Test()
    
else:
    print("Battery issue. Low battery voltage <3V. Stopped")
    badge.error.battery_low_critical()
        
#Everything ok
print("All ok!")
for x in range(3):
    time.sleep(0.1)
    badge.LEDs.BUSY.value = True
    badge.LEDs.HB.value = True
    time.sleep(0.1)
    badge.LEDs.BUSY.value = False
    badge.LEDs.HB.value = False

#test
testid = 0
testframes = 4
while testid<=testframes:
    dirs = os.listdir("images")
    for file in dirs:
        print("BENCH")
        #Load
        timefirst = time.monotonic()
        bmp = BMP.bitmap("images/" + file)
        delay = time.monotonic() - timefirst        
        print("Image load delay in ms")
        print(delay*1000)          
        
        #Generate
        timefirst = time.monotonic()
        image = bmp.generate1bit_array()
        delay = time.monotonic() - timefirst        
        print("Image generation delay in ms")
        print(delay*1000)
        
        #Store frame
        timefirst = time.monotonic()
        badge.OLED.store_frame(image, 0)
        delay = time.monotonic() - timefirst        
        print("Frame storing delay in ms")
        print(delay*1000)           

        #Show frame
        timefirst = time.monotonic()
        badge.OLED.show_frame(testid)
        delay = time.monotonic() - timefirst        
        print("Frame drawing delay in ms")
        print(delay*1000)  
        testid=testid+1
        
        time.sleep(0.1)

testid = 0
while True:
    badge.OLED.show_frame(testid%3)
    testid = testid + 1
    time.sleep(1/30)
    
#hold
while True:
    time.sleep(1)
    badge.LEDs.HB.value = False
    time.sleep(1)
    badge.LEDs.HB.value = True    
