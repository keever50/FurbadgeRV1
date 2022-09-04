print("MENU")

    
import time, os, traceback, sys
from badge import battery, OLED, IOInterface, error
#Text = 6X 7Y

exec(open("programs/cursortest.py").read())
    
#Controls
OLED.driver.text("UP",0,0,255)
OLED.driver.text("DWN",0,32-7,255)
OLED.driver.text("XX",126-(6*2),0,255)
OLED.driver.text("X",126-6,32-7,255)
#List
OLED.driver.line(6*3,0,6*3,32,1)
OLED.driver.line(128-(6*3),0,128-(6*3),32,1)

#Programs
index = 0
for entry in os.listdir("programs"):
    print(entry)
    OLED.driver.text(entry,(6*3)+5,index*7,255)
    index=index+1
    
    time.sleep(0.1)
    OLED.driver.show()
    
OLED.driver.line((6*3),3,(6*3)+4,3,1)
OLED.driver.show()


while True:
    IOInterface.HB.value = True
    time.sleep(0.01)
    IOInterface.HB.value = False
    time.sleep(2)
    
    if IOInterface.joystick_P.value != True:
        break

#exec(open("programs/imagetest.py").read())