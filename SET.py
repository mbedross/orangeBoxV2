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

def valve(vNumber, state):
    """
    This module operates the valves around the sample chamber. 
    
    Input Variables:
    vNumber = the valve number to be operated (can be scalar or vector for multiple
              valves). vNumber = header.valveRelayXXX
    state = desired state of the valve. 0 = open, 1 = closed
    
    NOTE: Valves are NORMALLY OPEN (N.O.)
    """
    try:
        for x in range(0, len(vNumber)-1):
            os.system('echo "%d" |sudo tee /sys/class/gpio/gpio%s/value' %(state, vNumber[x]))
            statusLED(vnumber[x], state)
        if state == 0:
            status = "opened"
        else:
            status = "closed"
        message = "Valve(s)", vNumber, "have been %s" %(status)
        PRINT.event(message)
    except Exception as e:
        message = "Valve %d was unable to be set. Error is as follows:\n" %(vNumber)
        PRINT.event(message)
        PRINT.event(e)
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
        for x in range(0, len(relayNumber)-1):
            os.system('echo "%d" |sudo tee /sys/class/gpio/gpio%s/value' %(state, relayNumber[x]))
            if relayNumber[x] == header.laserRelay:
                header.statusLaser = state
                if state == 0:
                    message = "The laser has been shut off"
                    PRINT.event(message)
                else:
                    message = "The laser has been turned on"
                    PRINT.event(message)
            if relayNumber[x] == header.pumpRelay:
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

