from badge import IOInterface
from badge import error

#Configurable
critical_voltage = 2.8

#Battery check can shut down the program when voltage is below critical. Normally returns voltage
def check():
    BATV = IOInterface.battery_voltage()
    if critical_voltage < critical_voltage:
        error.battery_low_critical()
    return BATV