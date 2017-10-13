"""

Date Created: 2017.10.10

This script is the intializing and main wrapper function that controls the DHM.
This script is responsible for initializing the instrument, communicating with
the host computer (if present).

"""

import socket
import time
import datetime
import re
import subprocess
import GET
import PRINT
import RUN
import SET
import header
header.init()

## Initialize all GPIO pins
header.defineGPIO()

## Turn on the 'busy' LED to let user(s) know start has begun
SET.LED(header.LEDbusy, 1)

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
RUN.connectUDP()

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
