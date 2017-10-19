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
import os
import header
header.init()

def LED(pinNumber, state):
    os.system('echo %d > /sys/class/gpio/gpio%d/value' %(state, pinNumber))
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

def powerRelay(relayNumber, state):
    try:
        if relayNumber == "all":
            for x in range(0, len(header.relayALL)-1):
                os.system('echo "%d" |sudo tee /sys/class/gpio/gpio%s/value' %(state, header.relayALL[x]))
            if state == 0:
                message = "All relays have been turned off"
            else:
                message = "All relays have been turned on"
            PRINT.event(message)
        for x in range(0, len(relayNumber)-1):
            os.system('echo "%d" |sudo tee /sys/class/gpio/gpio%s/value' %(state, relayNumber[x]))
            if relayNumber[x] == header.relayLaser:
                header.statusLaser = state
                if state == 0:
                    message = "The laser has been shut off"
                    PRINT.event(message)
                else:
                    message = "The laser has been turned on"
                    PRINT.event(message)
            if relayNumber[x] == header.relayPump:
                header.statusPump = state
                if state == 0:
                    message = "The pump has been shut off"
                    PRINT.event(message)
                else:
                    message = "The pump has been turned on"
                    PRINT.event(message)
    except Exception as e:
        message = "Power Relay %d was unable to be set. Error is as follows:" %(relayNumber[x])
        PRINT.event(message)
        PRINT.event(e)
    return

