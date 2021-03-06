"""
Date Created:       2017.09.11
Date Last Modified: 2017.11.03

This script contains all executable modules that are designated as SET commands

Example:
In the main python script, import this script and run the desired module as such:

import SET
SET.module(inputs)

"""

import PRINT
import GET
import os
import socket
import header
header.init()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

def GPIO(pinNumber, state):
    Error = False
    try:
        for x in range(0, len(pinNumber)-1):
            os.system('echo "%d" |sudo tee /sys/class/gpio/gpio%s/value' %(state[x], pinNumber[x]))
            message = "GPIO Pin #%d (relay) has been set to %d" %(pinNumber[x], state[x])
    except Exception as Error:
        message = "Power Relay %d was unable to be set. Error is as follows:" %(pinNumber[x])
        PRINT.event(message)
        PRINT.event(Error)
    return (Error)

def arduinoPin(pinNumber, state):
    for x in range(0, len(pinNumber)-1):
        Pin = GET.arduinoSyntax(pinNumber[x], state[x])
        s.connect((header.VS_IP, header.VS_PORT))
        s.sendall(Pin)
        pinState = int(s.recv(1024))
        s.close()
        ## Check if pinState contains error information
        Error[x] = GET.isError(pinState)
    return (Error)