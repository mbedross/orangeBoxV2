"""
Date Created:       2017.09.10
Date Last Modified: 2017.09.11

This script contains all executable modules that are designated as RUN commands

Example:
In the main python script, import this script and run the desired module as such:

import RUN
RUN.module(inputs)

"""

import socket
import os
import os.path
import time
import math
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
    
    ## First make sure all valves are open before pump turns on
    if header.valve1 == 1:
        vNumber = header.valve1
        state = 0
        SET.valve(vNumber, state)
    if header.valve2 == 1:
        vNumber = header.valve1
        state = 0
        SET.valve(vNumber, state)
    
    lock = True

    while lock != False:
        os.system('echo "1" |sudo tee /sys/class/gpio/gpio%s/value' %(header.pumpRelay))
        time.sleep(0.2)
        os.system('echo "0" |sudo tee /sys/class/gpio/gpio%s/value' %(header.pumpRelay))
        time.sleep(0.2)
        lock = os.path.isfile(header.pumpLock)
        
    os.system('echo "0" |sudo tee /sys/class/gpio/gpio%s/value' %(header.pumpRelay))
    return

def connectUDP():
    """
    
    This module connects the DHM to the host computer via UDP. This script is only
    intended to be ran once at start up. Once the connection is established, the
    DHM sends an intiating message to the host computer
    
    """
    message = "UDP target IP: %s, UDP target port: %d" % (UDP_IP, UDP_PORT)
    PRINT.event(message)
    
    ## Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    message = "Socket created: %s:%d" % (header.UDP_IP, header.UDP_PORT)
    PRINT.event(message)
    PRINT.udp(message)
    
    ## Send MESSAGE to verify connection
    sock.sendto(MESSAGE, (header.UDP_IP, header.UDP_PORT))
    
    message = "Initialization message sent over UDP, now awaiting commands..."
    PRINT.event(message)
    PRINT.udp(message)
    return

def powerOFF():
    ## Make sure all valves and power relays are off (valves are normally open)
    vNumber = [header.valve1, header.valve2, header.valve3]
    state = 0
    SET.valve(vNumber, state)
    rNumber = [header.laserRelay, header.pumpRelay]
    SET.powerRelay(rNumber, state)
    
    message = "Non-emergency shut down"
    PRINT.event(message)
    PRINT.udp(message)
    
    ## wait for 5 seconds
    time.sleep(5)
    
    # Shut down
    os.system('shutdown -P now')
    return

def EMERGENCYoff():
    ## This call is similiar to a hard power off, it doesnt wait for current programs
    ## to end or to unmount any drives, it immediately calls for a reboot (but
    ## remain powered off)
    PRINT.emergency('Emergency shut off now!, look at previous event for error details.')
    os.system('echo 1 > /proc/sys/kernel/sysrq && echo b > /proc/sysrq-trigger')
    return
