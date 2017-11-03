"""
This file is non-executable!
This is for organizational purposes only so that this subroutine can be used in 
other codes for LINUX

file = filepath the print command is going to print to
"""

import serial

def connect():
    
    ser = serial.Serial("/dev/ttyACM0", baudrate = 19200)

    ## open serial ports if closed
    if(ser.isOpen() == False):
        ser.open()

def disconnect():

    if(ser.isOpen() == True):
        ser.close()
