import time

from badge import OLED
from badge import IOInterface
from badge import battery

def battery_low_critical():
    print("Battery voltage critical")
    turnoff()
    
    while True:
        #Battery error loop
        IOInterface.HB.value = True
        time.sleep(0.01)
        IOInterface.HB.value = False
        time.sleep(2)

def trap():
    print("Main exitted")
    turnoff()
    while True:
        battery.check()
        time.sleep(1)
        IOInterface.HB.value = False
        time.sleep(1)
        IOInterface.HB.value = True
    
def turnoff():
    OLED.driver.fill(0)
    OLED.driver.show()
    OLED.Power(False)      