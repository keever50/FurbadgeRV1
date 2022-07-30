import time

from badge import OLED
from badge import LEDs

def battery_low_critical():
    print("Battery voltage critical")
    OLED.Power(False)  
    
    while True:
        #Battery error loop
        LEDs.HB.value = True
        time.sleep(0.01)
        LEDs.HB.value = False
        time.sleep(2)

         