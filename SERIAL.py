"""
Date Created:       2017.11.02
Date Last Modified: 2017.11.03

This script is to be run by the main python script as a subprocess. It acts as a
virtual server that facilitates communication to and from the arduino.

"""

import socket
import serial
import header
header.init()


## Establish virtual server IP and Port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((header.VS_IP, header.VS_PORT))
s.listen(1)

## Establish serial connection with arduino
ser = serial.Serial(header.arduinoPort, baudrate = header.baudRate)
## open serial ports if closed
if(ser.isOpen() == False):
    ser.open()

while True:
    conn, addr = s.accept()      ## Wait forever for a connection
    data = conn.recv(1024)
    Pin = str.encode(data)
    ser.write(Pin)
    
    ## Once the command is sent to arduino, a response is expected.
    tdata = ser.read()           ## Wait forever for a command
    time.sleep(1)                ## Sleep (or inWaiting() doesn't give the correct value)
    data_left = s.inWaiting()    ## Get the number of characters ready to be read
    tdata += ser.read(data_left) ## Do the read and combine it with the first character
    ## Send the received serial packet to client server
    conn.sendall(tdata)
    conn.close()                 ## Once a connection and data are received, close port
    
