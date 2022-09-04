import time, os
from badge import battery, OLED, error
from badge import IOInterface as IO

X = 0
Y = 0
Update = True
while True:
    time.sleep(1/30)
    
    if Update == True:
        Update = False
        OLED.driver.fill(0)
        OLED.driver.pixel(X,Y,1)
        OLED.driver.show()
    
    #Input
    if IO.joystick_RD.value != True:
        X = X + 1
        Y = Y + 1
        Update = True
    if IO.joystick_LU.value != True:
        X = X - 1
        Y = Y - 1
        Update = True
    if IO.joystick_RU.value != True:
        X = X + 1
        Y = Y - 1
        Update = True
    if IO.joystick_LD.value != True:
        X = X - 1
        Y = Y + 1
        Update = True
    if IO.joystick_P.value != True:
        break
    
    IOInterface.HB.value = not IOInterface.HB.value
    