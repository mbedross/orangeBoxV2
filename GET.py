"""

Date Created: 2017.09.13
Date Last Modified: 2017.09.13

This script contains all modules of type GET. These modules are meant as queries
to current system statuses as well as to query current system time

Example:
In the main python script, import this script and run the desired module as such:

import GET
(output) = GET.module(inputs)

"""

import time
import header
header.init()

def serialRead():
    while 1:
        tdata = ser.read()           # Wait forever for anything
        time.sleep(1)              # Sleep (or inWaiting() doesn't give the correct value)
        data_left = s.inWaiting()  # Get the number of characters ready to be read
        tdata += ser.read(data_left) # Do the read and combine it with the first character
        break
    return tdata

def pump():
    lock = os.path.isfile(header.pumpLock)
    if lock == True:
        pump = 1
    else:
        pump = 0
    return pump

def temp():
    Pin = str.encode(header.tempPower[0])
    ser.write(Pin)
    Temps = serialRead()
    """
    TO BE WRITTEN/REVISED
    
    The arduino takes care of all the temp reading stuff (like the Steinhart-Hart 
    equation and sends out the temperatures one by one (EOL in between) through
    the serial port. The question is: does GET.Serial() catch all five temperatures
    our does it have to be modified to catch all five. AND after it catches all five
    what would the string look like? How can temperature (numbers) be extracted from the string?
    """
    return Temps

def relay(relayNumber):
    for x in range(0, len(relayNumber)-1):
        relayState[x] = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(relayNumber[x]))
    return (relayState)

def arduinoRelay(relayNumber):
    for x in range(0, len(relayNumber)-1):
        Pin = relayNumber[x] + 0.2      ## the 0.2 tells the arduino to query pin state
        Pin = str.encode(Pin)
        ser.write(Pin)
        relayState[x] = serialRead()
    return (relayState)
