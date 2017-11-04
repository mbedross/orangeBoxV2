"""
Date Created:       2017.09.10
Date Last Modified: 2017.11.03

This script runs the pump. Because this script continuously monitors the existance of the lock file, it has been written as a separate function so it can be called as a subprocess

"""

import os
import os.path
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

pump()