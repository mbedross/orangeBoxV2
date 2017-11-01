"""
Date Created:       2017.09.11
Date Last Modified: 2017.09.11

This script contains all executable modules that are designated as SET commands

Example:
In the main python script, import this script and run the desired module as such:

import SET
SET.module(inputs)

"""

import PRINT
import GET
import os
import header
header.init()

def LED(pinNumber):
    ## All LED's are now controlled by the Arduino 101
    Pin = str.encode(pinNumber)
    ser.write(Pin)
    Message = GET.Serial()
    if Message != pinNumber:
        message = "Something went wrong while turnin LED %d on/off. Message from arduino is as follows:" %(pinNumber)
        PRINT.event(message)
        PRINT.event(Message)
    else:
        message = "LED %d successfully switched on/off" %(pinNumber)
        PRINT.event(message)
    return

def DAQtime(daqTime):
    try:
        header.DAQtime = daqTime
        message = "DAQ time changed to %f seconds" % (daqTime)
        PRINT.event(message)
    except Exception as e:
        message = "DAQ time wasunable to be set. Error is as follows:\n"
        PRINT.event(message)
        PRINT.event(e)
    return

def relay(relayNumber, state):
    try:
        for x in range(0, len(relayNumber)-1):
            os.system('echo "%d" |sudo tee /sys/class/gpio/gpio%s/value' %(state[x], relayNumber[x]))
            message = "GPIO Pin #%d (relay) has been set to %d" %(relayNumber[x], state[x])
    except Exception as e:
        message = "Power Relay %d was unable to be set. Error is as follows:" %(relayNumber[x])
        PRINT.event(message)
        PRINT.event(e)
    return

def arduinoRelay(relayNumber, state):
    try:
        for x in range(0, len(relayNumber)-1):
            Pin = str.encode(relayNumber[x])
            ser.write(Pin)
            Message = GET.Serial
            if Message != relayNumber[x]:
                message = "Something went wrong. Arduino error is as follows:"
                PRINT.event(message)
                PRINT.event(Message)
            else:
                message = "Arduino relay %d was set to %d" %(relayNumber, state)
                PRINT.event(mesage)
            time.sleep(0.5)    ## Allow time for action to execute before going to bext iteration
    except Exception as e:
        message = "Power Relay %d was unable to be set. Error is as follows:" %(relayNumber[x])
        PRINT.event(message)
        PRINT.event(e)
    return