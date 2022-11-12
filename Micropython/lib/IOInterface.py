from machine import Pin, ADC
import machine

#Heartbeat LED
HB = Pin(25, Pin.OUT) 
HB.high()
booster = Pin(24, Pin.OUT)


#The badge joystick is rotated by 45 degrees. (Totally not a design error)
class Joystick:
    LU = Pin(14, Pin.IN, pull=Pin.PULL_UP)  #Left up
    LD = Pin(12, Pin.IN, pull=Pin.PULL_UP)  #Left down 
    RU = Pin(13, Pin.IN, pull=Pin.PULL_UP)  #Right up
    RD = Pin(15, Pin.IN, pull=Pin.PULL_UP)  #Right down
    P = Pin(20, Pin.IN, pull=Pin.PULL_UP)   #Press

    def getDirection():
        X = 0
        Y = 0
        #Corners
        if not Joystick.LU.value(): 
            X = -0.707
            Y = -0.707
        if not Joystick.RU.value(): 
            X = 0.707 
            Y = -0.707
        if not Joystick.LD.value(): 
            X = -0.707 
            Y = 0.707
        if not Joystick.RD.value(): 
            X = 0.707 
            Y = 0.707

        #X
        if not Joystick.RU.value() and not Joystick.RD.value(): 
            X = 1
            Y = 0
        if not Joystick.LU.value() and not Joystick.LD.value(): 
            X = -1
            Y = 0
        #Y
        if not Joystick.RU.value() and not Joystick.LU.value(): 
            Y = -1 
            X = 0
        if not Joystick.RD.value() and not Joystick.LD.value(): 
            Y = 1
            X = 0

        
        return X, Y

class Battery:
    BAT_ADC = ADC(26)
    BAT_MIN_V = 3.4
    BAT_MAX_V = 4.1

    def get_voltage():
        return Battery.BAT_ADC.read_u16()/9930

    def get_percentage():
        return min((Battery.get_voltage()-Battery.BAT_MIN_V)/(Battery.BAT_MAX_V-Battery.BAT_MIN_V)*100,100)

    def safety_check():
        if Battery.get_percentage() <= 0:
            print("Battery empty. Processor going into deepsleep")
            booster.low()
            machine.deepsleep()