"""

Date Created:       2017.09.16
Date Last Modified: 2017.09.18

This script is for the sole purpose of monitoring the battery in the
instrument. This is both a voltage based SoC measurement and a Coulomb counter.
Both are needed because although Coulomb counting is good for metering the energy
used by the battery, it cannot measure the charge currenly present in the battery.
For this, it needs to infer on the initial state of charge on a corrlation between
SoC and voltage across the battery. Coulomb counting is done by measuring the voltage
across a shunt resistor and integrating V/R over time.

This script should be called as a subprocess by the main python function

"""
import PRINT
import RUN
import time
try:
    import scipy
except ImportError:
    PRINT.event("Import Error: SciPy")
try:
    import pandas as pd
except ImportError:
    PRINT.event("Import Error: Pandas")
import header
header.init()

compOverhead = 0.3

## First, the voltage across the battery must be read
initVoltage = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.batterV))

"""
To be inserted!!! From the previous line, interpolate the total amunt of
energy remaining in the battery, store this variable as energyRemaining
"""

while True:
    ## Read voltage accross shunt resistor
    header.shuntV = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.shuntV))
    
    ## Using Ohm's law, going from voltage to current is done by dividing voltage by resistance
    ## Shunt resistance is defined in header.py as header.Rshunt
    current = header.shuntV/header.Rshunt
    ## Energy in Ah is calculated by multiplying current by sample time of 1 second
    energy = current/3600
    energyRemaining = energyRemaining - energy
    
    SoC = (header.batCap-energyRemaining)/header.batCap
    if (SoC > 0.75 and SoC <= 1):
        ## If the battery is between 75-100% SoC, turn the Green LED on
        os.system('echo 0 > /sys/class/gpio/gpio%d/value' %(header.LEDbatR))
        os.system('echo 0 > /sys/class/gpio/gpio%d/value' %(header.LEDbatY))
        os.system('echo 1 > /sys/class/gpio/gpio%d/value' %(header.LEDbatG))
    
    if (SoC > 0.4 and SoC <= 0.75):
        ## If the battery is between 40-75% SoC, turn the Yellow LED on
        os.system('echo 0 > /sys/class/gpio/gpio%d/value' %(header.LEDbatR))
        os.system('echo 0 > /sys/class/gpio/gpio%d/value' %(header.LEDbatG))
        os.system('echo 1 > /sys/class/gpio/gpio%d/value' %(header.LEDbatY))
    
    if (SoC > 0 and SoC <=0.4):
        ## If the battery is between 0-40% SoC, turn the Red LED on
        os.system('echo 0 > /sys/class/gpio/gpio%d/value' %(header.LEDbatY))
        os.system('echo 0 > /sys/class/gpio/gpio%d/value' %(header.LEDbatG))
        os.system('echo 1 > /sys/class/gpio/gpio%d/value' %(header.LEDbatR))
    
    if SoC < 0.05:
        ## The battery has <=5% battery left. Send a message to host server and shut down
        message = 'DHM has less than 5% battery remaining, will shut down in 10 seconds'
        PRINT.event(message)
        PRINT.UDP(message)
        time.sleep(10)
        RUN.powerOFF()
    
    time.sleep(1-compOverhead)
        
        
    
    