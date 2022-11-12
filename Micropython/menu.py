import UI 
import OLED
import IOInterface as IO
import time

OLED.power_on()

FP = UI.FilePicker()

FP.open("sys_programs")

while True:
    OLED.driver.fill(0)
    OLED.driver.text(str(IO.Battery.get_voltage()),0,0,1)
    OLED.driver.text(str(IO.Battery.get_percentage()),0,8,1)
    OLED.driver.show()
    time.sleep(1)
    
