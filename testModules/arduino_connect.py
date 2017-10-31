"""
This file is non-executable!
This is for organizational purposes only so that this subroutine can be used in 
other codes for LINUX

file = filepath the print command is going to print to
"""

import serial
import time
import datetime

ser = serial.Serial("/dev/ttyACM1", baudrate = 9600)

## open serial ports if closed
if(ser.isOpen() == False):
    ser.open()

def arduino_connect(file):
    
    connected = False;        ##(this is a logical statement to make connection
    while not connected:
        serin     = ser.read()
        connected = True
        ts        = time.time()
    	st        = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print >>file, st, " - Arduino Connected"
    return