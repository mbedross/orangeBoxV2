"""

Date Created:       2017.09.13
Date Last Modified: 2017.11.03

This script contains all modules of type GET. These modules are meant as queries
to current system statuses as well as to query current system time

Example:
In the main python script, import this script and run the desired module as such:

import GET
(output) = GET.module(inputs)

"""

import socket
import header
header.init()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def isError(dataSent, dataRecv):
    ## This module is to check whether or not a serial data packet from the 
    ## arduino contains error information.
    ## This is written as a separate module so error definitions can be changed
    ## easily.
    if (dataSent == dataRecv):
        Error = False
    else:
        Error = True
    return Error

def arduinoSyntax(pinNumber, action):
    if (action == "on"):
        rem = 1
    if (action == "off"):
        rem = 0
    if (action == "state"):
        rem = 2
    formatted = 10*pinNumber+rem
    return (formatted)

def pump():
    lock = os.path.isfile(header.pumpLock)
    if lock == True:
        pump = 1
    else:
        pump = 0
    return pump

def temp():
    Pin = str.encode(header.tempPower[0])
    ser.write(Pin)
    Temps = serialRead()
    """
    TO BE WRITTEN/REVISED
    
    The arduino takes care of all the temp reading stuff (like the Steinhart-Hart 
    equation and sends out the temperatures one by one (EOL in between) through
    the serial port. The question is: does GET.Serial() catch all five temperatures
    our does it have to be modified to catch all five. AND after it catches all five
    what would the string look like? How can temperature (numbers) be extracted from the string?
    """
    return Temps

def GPIO(pinNumber):
    for x in range(0, len(pinNumber)-1):
        pinState[x] = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(pinNumber[x]))
    return (pinState)

def arduinoPin(pinNumber):
    for x in range(0, len(pinNumber)-1):
        Pin = arduinoSyntax(pinNumber[x], "state")
        s.connect((header.VS_IP, header.VS_PORT))
        s.sendall(Pin)
        pinState[x] = int(s.recv(1024))
        s.close()
    return (pinState)