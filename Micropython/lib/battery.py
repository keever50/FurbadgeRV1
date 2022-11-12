from machine import Timer
import IOInterface as IO
import OLED
import machine 
import time

BATTERY_CHECK_PERIOD = 2000

def battery_check(d):
    if IO.Battery.get_percentage() <= 5:
        IO.HB.low()
        OLED.driver.fill(0)
        OLED.driver.text("BATTERY TOO LOW",0,0,1)
        OLED.driver.show()
        time.sleep(5)
        OLED.driver.fill(0)
        OLED.driver.show()
        OLED.power_off()
        #machine.deepsleep()
        while True:
            machine.lightsleep(1000)
            IO.HB.high()
            machine.lightsleep(10)
            IO.HB.low()
            

battery_timer = Timer(period=BATTERY_CHECK_PERIOD,mode=Timer.PERIODIC,callback=battery_check)    

