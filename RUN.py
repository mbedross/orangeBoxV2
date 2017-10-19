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
    if header.relayValve1 == 1:
        vNumber = header.relayValve1
        state = 0
        SET.valve(vNumber, state)
    if header.relayValve2 == 1:
        vNumber = header.relayValve2
        state = 0
        SET.valve(vNumber, state)
    
    lock = True

    while lock != False:
        os.system('echo "1" |sudo tee /sys/class/gpio/gpio%s/value' %(header.relayPump))
        time.sleep(0.2)
        os.system('echo "0" |sudo tee /sys/class/gpio/gpio%s/value' %(header.relayPump))
        time.sleep(0.2)
        lock = os.path.isfile(header.pumpLock)
        
    os.system('echo "0" |sudo tee /sys/class/gpio/gpio%s/value' %(header.relayPump))
    return

def connectUDP():
    """
    
    This module connects the DHM to the host computer via UDP. This script is only
    intended to be ran once at start up. Once the connection is established, the
    DHM sends an intiating message to the host computer
    
    """
    message = "UDP target IP: %s, UDP target port: %d" % (header.UDP_IP, header.UDP_PORT)
    PRINT.event(message)
    
    try:
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
        header.connected = 1
    except Exception as e:
        message = "UDP connection failed with following error:"
        PRINT.event(message)
        PRINT.event(e)
    return

def rampLaserUP():
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

def rampLaserDOWN():
    """
    IMPORTANT!!!
    
    This code is TENTATIVE. Must first test if PWM is valid with the laser driver
    If not, ramping is not possible, must design a voltage divider such that the
    max output of the GPIO (1.8V) gives the desired optical power desired
    """
    t_ramp = 5  ## Time in seconds to ramp up laser
    v_now=0.394
    v_low = 0
    for t in range(0,t_ramp):
        v_new = v_now-v_high/t_ramp
        os.system('/home/shamu/mcc-libhid/write_DtoA_channel 0 %f' % (v_new))
        v_now = v_new
        time.sleep(1)
    message = "Laser finished ramping DOWN and is OFF"
    PRINT.event(message)
    return

def powerOFF():
    ## Ramp down laser
    rampLaserDown()
    ## Make sure all valves and power relays are off (valves are normally open)
    state = 0
    SET.powerRelay("all", state)
    
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
