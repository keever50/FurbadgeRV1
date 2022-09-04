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

#Joystick
joystick_LU = digitalio.DigitalInOut(board.GP14)
joystick_LU.direction = digitalio.Direction.INPUT
joystick_LU.pull = digitalio.Pull.UP

joystick_LD = digitalio.DigitalInOut(board.GP12)
joystick_LD.direction = digitalio.Direction.INPUT
joystick_LD.pull = digitalio.Pull.UP

joystick_RU = digitalio.DigitalInOut(board.GP13)
joystick_RU.direction = digitalio.Direction.INPUT
joystick_RU.pull = digitalio.Pull.UP

joystick_RD = digitalio.DigitalInOut(board.GP15)
joystick_RD.direction = digitalio.Direction.INPUT
joystick_RD.pull = digitalio.Pull.UP

joystick_P = digitalio.DigitalInOut(board.GP20)
joystick_P.direction = digitalio.Direction.INPUT
joystick_P.pull = digitalio.Pull.UP
