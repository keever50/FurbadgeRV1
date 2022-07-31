#Importing
import board
import busio
import digitalio
import time
import microcontroller
import os
import analogio

#Badge libs/drivers
from badge import OLED
from badge import error
from badge import LEDs

##INIT##

#Battery check
BATV_PIN = analogio.AnalogIn(board.GP26)
BATV = (BATV_PIN.value*6.6) / 65536
print("Battery voltage check: BATV = {:5.2f}V".format(BATV) )

if BATV >= 3:
    print("Battery OK. Turning on OLED circuit")
    print("[OLED]Powering on")
    OLED.Power(True)
    print("[OLED]Testing")
    OLED.Test()
    
else:
    print("Battery issue. Low battery voltage <3V. Stopped")
    error.battery_low_critical()
        
  

# :)


#Everything ok
print("All ok!")
for x in range(3):
    time.sleep(0.1)
    LEDs.BUSY.value = True
    LEDs.HB.value = True
    time.sleep(0.1)
    LEDs.BUSY.value = False
    LEDs.HB.value = False

#hold
while True:
    time.sleep(1)
    LEDs.HB.value = False
    time.sleep(1)
    LEDs.HB.value = True    
