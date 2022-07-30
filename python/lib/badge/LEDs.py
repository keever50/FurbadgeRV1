import board
import busio
import digitalio

#Heartbeat
HB = digitalio.DigitalInOut(board.GP25)
HB.direction = digitalio.Direction.OUTPUT
#Busy indicator
BUSY = digitalio.DigitalInOut(board.GP1)
BUSY.direction = digitalio.Direction.OUTPUT

#init indicator
HB.value = True

