"""
Date Created: 2017.10.10

This script monitors the laser diode current. It can turn the laser off if diode
current hits a critical value (TBD mA)

This script should be called as a subproccess by the main function so it can run
continuously in the background

"""

import time
import SET
import PRINT
import header
header.init()

def readCurrent():
    ## Read the laser diode current
    voltage = int(open(header.diodeC).read())
    """
    TO BE WRITTEN:
    Convert the ADC value of voltage to actual voltage in mV
    
    """
    ## To convert from voltage to diode current, the conversion is 10 mV = 1 mA
    ## Nominal operating current for 405 nm laser is 50 mA (60 mA absolute max)
    current = voltage/10

while True:
    readCurrent()
    if current >= 60:
        ## Laser diode is now in over current mode, will check current in two seconds,
        ## if still high, error message will be printed and laser shut off
        time.sleep(2)
        readCurrent()
        if current >= 60:
            message = "Laser current has been above 60 mA for more than two seconds, shutting off laser now"
            PRINT.event(message)
            RUN.laserRampDOWN()
            SET.powerRelay(header.laserRelay, 0)
            message = "Laser is now OFF"
            PRINT.event(message)
    time.sleep(1)
            
    
    