import time

##INIT##
from badge import battery, OLED, IOInterface, error

#Battery check
battery.check() #Can stop code
print("Battery OK. Turning on OLED circuit")
print("[OLED]Powering on")
OLED.Power(True)
print("[OLED]Testing")
OLED.Test()

#Everything ok
print("All ok!")
for x in range(3):
    time.sleep(0.1)
    IOInterface.BUSY.value = True
    IOInterface.HB.value = True
    time.sleep(0.1)
    IOInterface.BUSY.value = False
    IOInterface.HB.value = False

#Run menu
exec(open("programs/menu.py").read())

#trap
error.trap()  
