"""

Date Created: 2017.10.10

This script is the intializing and main wrapper function that controls the DHM.
This script is responsible for initializing the instrument, communicating with
the host computer (if present).

"""

import socket
import subprocess
import GET
import PRINT
import RUN
import SET
import __init__
import header
header.init()

def connectUDP():
    """
    
    This module connects the DHM to the host computer via UDP. This script is only
    intended to be ran once at start up. Once the connection is established, the
    DHM sends an intiating message to the host computer
    
    """
    message = "UDP target IP: %s, UDP target port: %d" % (header.UDP_IP, header.UDP_PORT)
    PRINT.event(message)
    
    try:
        global sock
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

## Initialize all GPIO pins
__init__.exportGPIO(header.GPIO)
__init__.defineGPIO(header.GPIO)

## Establish Serial Connection with Arduino 101
__init__.connectArduino(header.arduinoPort)

if header.connected == 1:
    ## If UDP connection is established, sync CPU time with host server
    __init__.syncTime()


## Turn on the 'busy' LED to let user(s) know start has begun
SET.LED(header.LEDbusy[0])
## Update LEDbusy state to 1
header.LEDbusy[1] = 1

## Begin monitoring moisture sensors
## This is called by a subprocess in order to run in the background
Moist = subprocess.Popen(["sudo","%s/moistureSensors.py" % (header.codeFolder)])

## Begin monitoring battery State of Charge (SoC)
## This is called by a subprocess in order to run in the background
Battery = subprocess.Popen(["sudo","%s/batteryStatus.py" % (header.codeFolder)])

## Begin monitoring physical operation buttons
## This is called by a subprocess in order to run in the background
Buttons = subprocess.Popen(["sudo","%s/checkButtons.py" % (header.codeFolder)])

## Try to connect to UDP host
connectUDP()

## Syncronize time with Host server
__init__.syncTime()

## Turn the laser on and ramp it up to nominal operating conditions
SET.powerRelay(header.laserRelay, 1)
RUN.rampLaserUP()
## Begin monitoring laser diode current
## This is called by a subprocess in order to run in the background
Laser = subprocess.Popen(["sudo","%s/laserCurrent.py" % (header.codeFolder)])

## System initialization is now complete. Turn the 'ready light' on
SET.LED(header.LEDbusy, 0)
SET.LED(header.LEDready, 1)

if header.connect == 1:
    ## If header.connect = 1, then the DHM successfully connected to the host server via UDP so it will now listen for commands
    ## Begin waiting for commands from BRUIE
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if data:
            message = "Datagram Received:", data
            PRINT.event(message)
        
        if c in data: # DHM_record 
            ## TO BE WRITTEN
            RUN.DAQ() ## Placeholder
        
        if header.comStatus in data: # Host queried DHM status
            pump = GET.pump()
            relays = GET.relay("all")
            temp = GET.temp()
            message = 'Pump status is: ', pump, '\n', 'Relay statuses are: ', relays, '\n', 'Temperatures are : ', temp
            PRINT.udp(message)
        
        if header.comPumpOn in data: # Turn pump on
            header.touch(header.pumpLock)
            RUN.pump()
        
        if header.comPumpOff in data: # Turn pump off
            os.remove(pumpLock)
        
        if f in data: # run microscope on auto
            auto_run()
        
        if z in data: # Non-emergency shutdown
            power_off()
else:
    return
