"""
Date Created:       2017.09.10
Date Last Modified: 2017.11.03

This script contains all executable modules that are designated as RUN commands

Example:
In the main python script, import this script and run the desired module as such:

import RUN
RUN.module(inputs)

"""

import os
import os.path
import time
import PRINT
import SET
import header
header.init()

def pump():
    """
    This module runs the microfluidic pump on the DHM sample line
    
    Input Variables:
    This function will run as long as there is a pump lock file that exists. It
    will run the pump and check to see if the lock file exists after every pump cycle.
    Once the lock file is removed, the pump will be turned off.
                 
    """
    
    Error = SET.arduinoRelay(header.relayPump[0], "on")
    if (Error == False):
        header.relayPump[1] = 1
        message = "Pump is now on"
        PRINT.event(message)
    else:
        message = "Unknown error occured when trying to turn pump on"
        PRINT.event(message)
    
    ## Loop over lock file until it is deleted
    lock = True
    while lock != False:
        lock = os.path.isfile(header.pumpLock)
        
    Error = SET.arduinoRelay(header.relayPump[0], "off")
    if (Error == False):
        header.relayPump[1] = 1
        message = "Pump is now off"
        PRINT.event(message)
    else:
        message = "Unknown error occured when trying to turn pump off"
        PRINT.event(message)
    return

def laser():
    """
    IMPORTANT!!!
    
    This code is TENTATIVE. Must first test if PWM is valid with the laser driver
    If not, ramping is not possible, must design a voltage divider such that the
    max output of the GPIO (1.8V) gives the desired optical power desired
    """
    t_ramp = 5  ## Time in seconds to ramp up laser
    v_now=0
    v_high = 0.394
    for t in range(0,t_ramp):
        v_new = v_now+v_high/5
        os.system('/home/shamu/mcc-libhid/write_DtoA_channel 0 %f' % (v_new))
        v_now = v_new
        time.sleep(1)
    message = "Laser finished ramping UP and is ON"
    PRINT.event(message)
    return