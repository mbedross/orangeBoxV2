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

import header
header.init()
import math

def relay(relayNumber):
    if relayNumber == "all":
        for x in range(0, len(header.relayALL)-1):
            relayState[x] = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(relayNumber))
    else:
        relayState = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(relayNumber))
    return (relayState)

def pump():
    lock = os.path.isfile(header.pumpLock)
    if lock == True:
        pump = 1
    else:
        pump = 0
    return pump

def temp():
    
    ## Read temp sensors
    header.Temp[0] = int(open(header.temp1).read())
    header.Temp[1] = int(open(header.temp2).read())
    header.Temp[2] = int(open(header.temp3).read())
    header.Temp[3] = int(open(header.temp4).read())
    header.Temp[4] = int(open(header.tempSC).read())
    
    ## Now calculate temperatures
    bit = 12                # ADC bits
    bitDepth = math.pow(2,bit)
    
    for x in range(0, len(Temp)-1):
        Rt = ((bitDepth/header.Temp[x])-1)*header.R;
        logR = math.log(Rt);
        header.Temp[x] = 1 / (header.tempA + (header.tempB * logR) + (header.tempC * logR * logR * logR));
    
    return header.Temp