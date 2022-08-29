import board
import busio
import digitalio
import analogio

#Heartbeat
HB = digitalio.DigitalInOut(board.GP25)
HB.direction = digitalio.Direction.OUTPUT
#Busy indicator
BUSY = digitalio.DigitalInOut(board.GP1)
BUSY.direction = digitalio.Direction.OUTPUT

#init indicator
HB.value = True

#Battery check
BATV_PIN = analogio.AnalogIn(board.GP26)
def battery_voltage():
    return (BATV_PIN.value*6.6) / 65536