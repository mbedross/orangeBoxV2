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
import time
import math
import PRINT
import SET
import header
header.init()

def pump(STOP_pump, continuous):
    """
    This module runs the microfluidic pump on the DHM sample line
    
    Input Variables:
    STOP_pump = desired time to run the pump in seconds (should be an integer)
    continuous = logical value to decide if the pump should be run continuously
                 0 = NOT continuous, else run continuously
                 
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
    
    pumpFreq = 5                                         ## Pump frequency in Hz
    if continuous == 0:
        message = "Pump started"
        PRINT.event(message)
        
        totalCount = math.floor(STOP_pump*pumpFreq)
        count = 1
        while (count < totalCount):
            os.system('echo "1" |sudo tee /sys/class/gpio/gpio%s/value' %(header.pumpRelay))
            time.sleep(0.03)
            os.system('echo "0" |sudo tee /sys/class/gpio/gpio%s/value' %(header.pumpRelay))
            time.sleep(0.03)
            count = count + 1
        
        message = "Pump Stopped"
        PRINT.event(message)
        
    else:
        message = "Pump started"
        PRINT.event(message)
        
        while continuous != 0:
            os.system('echo "1" |sudo tee /sys/class/gpio/gpio%s/value' %(header.pumpRelay))
            time.sleep(0.03)
            os.system('echo "0" |sudo tee /sys/class/gpio/gpio%s/value' %(header.pumpRelay))
            time.sleep(0.03)
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
