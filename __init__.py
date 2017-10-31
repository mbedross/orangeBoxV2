"""
Date Created:       2017.10.25
Date Last Modified: 2017.10.25
Author: Manuel Bedrossian

This script contains all the modules used to initialize the DHM

NOTE: The module to connect with the host via UDP is not in this script because it must be in the main 

"""

import os
import serial
import PRINT
try:
    import ntplib
except Exception as e:
    message = "Error importing ntplib: message is as follows\n", e
    PRINT.event(message)

def exportGPIO(pins):
    """
    REMOVE AFTER DEBUGGING: The call might be...
    os.system('echo %d > /sys/class/gpio/export' %(header.XYZ))
    """
    ## This module exports all GPIO pins to be used
    for x in range(0, len(pins)-1):
        try:
            ## Export xth GPIO pin
            temp = pins[x]
            os.system('echo "%d" |sudo tee /sys/class/gpio/export' %(temp[0]))
        except Exception as e:
            message = "GPIO pin export failed.\n", e
            PRINT.event(message)
    return

def defineGPIO(pins):
    ## This module defines as used GPIO's as input/output as appropriate
    
    for x in range(0, len(pins)-1):
        try:
            temp = pins[x]
            if temp[1] == 1:
                direction = "in"
            else:
                direction = "out"
            ## Establish all push buttons as GPIO inputs
            os.system('echo %s > /sys/class/gpio/gpio%d/direction' %(direction, temp[0]))
        except Exception as e:
            message = "GPIO pin definition failed.\n", e
            PRINT.event(message)
    return

def syncTime():
    try:
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org')
        os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
        message = "Time syncronized with host server"
        PRINT.event(message)
    except Exception as e:
        message = "Could not sync time with host server. Error is as follows:\n", e
        PRINT.event(message)
    return

def connectArduino(arduinoPort):
    
    ser = serial.Serial(arduinoPort, baudrate = 19200)

    ## open serial ports if closed
    if(ser.isOpen() == False):
        ser.open()
    
    connected = False;        ##(this is a logical statement to make connection
    while not connected:
        serin     = ser.read()
        message = "Arduino Connected"
        PRINT.event(message)
        connected = True
    return