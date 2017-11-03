"""
Date Created:       2016.04.06
Date Last Modified: 2017.10.25
Author: Manuel Bedrossian

This is a header file for the operating system for the 2nd Gen. orangeBox DHM field
instrument. All global variables should be defined here to be used throughout all
dependent code.

Manu's MacBook Pro's IP in the wind tunnel is 192.168.1.14 (port is arbitrary)

"""

import os

def init():
    
    global fileFolder, codeFolder, pumpLock, camLock
    ## Identify eventlog directory
    filefolder = '/home/orangeboxv2/Desktop/EventLogs'
    ## Identify subroutine direcotry
    codefolder = '/home/orangeboxv2/Documents/holOS/orangeboxv2'
    ## Hardware lock files
    pumpLock = '/tmp/pumpLock.tmp'
    camLock = '/tmp/camLock.tmp'
    
    ## GPIO Pin numbers
    ## syntax: [pinNumber, type]
    ## type = 1 (input), type = 0 (output)
    ## NOTE: If a GPIO pin is added, be sure to add it to the global variable GPIO so it gets exported and defined
    ## Relays (all other relays are controlled through the Arduino)
    global relayLaser, relayTEC1, relayTEC2, relay2, relay3
    relayLaser = [346, 0]
    relayTEC1 =  [344, 0]
    relayTEC2 =  [351, 0]
    relay2 =     [499, 0]
    relay3 =     [497, 0]
    global laser, moistPower, moist1, moist2, moist3, moist4, batteryV, shuntV,diodeC
    #laser = 1                        ## GPIO laser optical power
    moistPower = [330, 0]            ## GPIO moisture sensor power
    moist1 =     [329, 1]            ## GPIO moisture sensor 1
    moist2 =     [332, 1]            ## GPIO moisture sensor 2
    moist3 =     [333, 1]            ## GPIO moisture sensor 3
    moist4 =     [336, 1]            ## GPIO moisture sensor 4
    #batteryV = 1                     ## battery voltage    (external ADC pin)
    #shuntV = 1                       ## system power shunt (external ADC pin)
    global buttonPump, buttonV1_2, buttonV3, buttonQuit, buttonDAQ
    buttonPump = [326, 1]            ## GPIO pump button
    buttonV1_2 = [347, 1]            ## GPIO Valve 1 and 2 button
    buttonV3 =   [349, 1]            ## GPIO Valve 3 button
    buttonQuit = [350, 1]            ## GPIO Quit button
    buttonDAQ =  [366, 1]            ## GPIO DAQ button
    ## With all GPIO pins defined, lump them all into one variable
    global GPIO
    GPIO = [relayLaser, relayTEC1, relayTEC2, relay2, relay3, moistPower, moist1, moist2, moist3, moist4, buttonPump, buttonV1_2, buttonV3, buttonQuit, buttonDAQ]
    
    ## Arduino Pins
    ## Analog Pins
    global temp1, temp2, temp3, temp4, tempSC, diodeC
    tempSC = 0                       ## temp sensor SC     (arduinoHeader.h)
    temp1 = 1                        ## temp sensor 1      (arduinoHeader.h)
    temp2 = 2                        ## temp sensor 2      (arduinoHeader.h)
    temp3 = 3                        ## temp sensor 3      (arduinoHeader.h)
    temp4 = 4                        ## temp sensor 4      (arduinoHeader.h)
    diodeC = 5                       ## laser diode sensor (arduinoHeader.h)
    # Digital Pins
    ## Syntax: pin = [pinNumber, state]
    global tempPower, relayPump, relayV1, relayV2, relayV3, LEDready, LEDbusy, LEDbatR, LEDbatY, LEDbatG
    tempPower = [2, 0]               ## Temp sensor power  (arduinoHeader.h)
    relayPump = [3, 0]               ## Pump   relay/LED   (arduinoHeader.h)
    relayV1 =   [4, 0]               ## Valve1 relay/LED   (arduinoHeader.h)
    relayV2 =   [5, 0]               ## Valve2 relay/LED   (arduinoHeader.h)
    relayV3 =   [6, 0]               ## Valve3 relay/LED   (arduinoHeader.h)
    LEDready =  [7, 0]               ## Ready LED [Green]  (arduinoHeader.h)
    LEDbusy =   [8, 0]               ## Busy  LED [Red]    (arduinoHeader.h)
    LEDbatR =   [9, 0]               ## SoC   LED [Red]    (arduinoHeader.h)
    LEDbatY =   [10, 0]              ## SoC   LED [Yellow] (arduinoHeader.h)
    LEDbatG =   [11, 0]              ## SoC   LED [Green]  (arduinoHeader.h)
    
    ## Status variables
    global statusLaser, statusCam, statusPump, statusV1, statusV1, statusV2, statusV3, statusM1, statusM2, statusM3, statusM4
    statusLaser = 0                  ## Laser status variable
    statusCam = 0                    ## Camera status variable
    
    ## Checking the status of the pump requires checking to see if the
    ## pumpLock file exists
    statusPump = os.path.isfile(header.pumpLock)
    
    ## Checking the status of the valve/moisture sensors requires checking the 
    ##GPIO pins associated with them
    statusV1 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.valve1))
    statusV2 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.valve2))
    statusV3 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.valve3))
    statusM1 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.moist1))
    statusM2 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.moist2))
    statusM3 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.moist3))
    statusM4 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.moist4))
    
    ## Misc. Global variables
    global pumpTime, DAQtime, ADC, UDP_IP, UDP_PORT, MESSAGE, tempA, tempB, tempC, Rtemp, Temp, Rshunt, batCap, connected, relayUDOO, relayArduino, arduinoPort, VS_IP, VS_PORT
    pumpTime = 10                      ## Pump time to cycle in new sample
    DAQtime = 15                       ## Standard image acq. time in seconds
    ADC = 24
    UDP_IP = "192.168.1.14"            ## IP address to host computer
    UDP_PORT = 5005                    ## UDP Port # to host computer
    VS_IP = "localhost"
    VS_PORT = 9988
    MESSAGE = "Hello, BRUIE! -DHM\n"   ## Sent to server to establish connection
    ## Constants for the Steinhart-Hart NTC Equation
    tempA = 0.0021879
    tempB = 0.0001248
    tempC = 0.0000013624
    Rtemp = 1500                           ## Reference Resistor value [Ohms]
    Temp = [0, 0, 0, 0, 0]             ## Variable to store temperatures
    Rshunt = 0.75                     ## Resistance of shunt resistor
    batCap = 100                      ## total usable battery capacity in Ah
    connected = 0;
    arduinoPort = "/dev/ttyACM0"
    baudRate = 19200
    relayUDOO = [relayLaser, relayTEC1, relayTEC2, relay2, relay3]
    relayArduino = [relayPump, relayV1, relayV2, relayV3]
    
    ## UDP command legend
    global comDAQ, comDAQstop, comStatus, comPumpOn, comPumpOff, comVinlet, comVoutlet, comVref, comDAQauto, comOFF
    comDAQ = 'DHM_record'                          # Start DAQ
    comDAQstop = 'DHM_stop'                        # Stop DAQ
    comStatus = 'DHM_status'                       # Query for DHM status
    comPumpOn = 'DHM_pumpOn'                       # Turn on pump
    comPumpOff = 'DHM_pumpOff'                     # Turn off pump
    comVinlet = 'DHM_invletValve'                  # Switch the sample chamber inlet valve
    comVoutlet = 'DHM_outletValve'                 # Switch the sample chamber outlet valve
    comVref = 'DHM_refValve'                       # Switch the reference channel valve
    comDAQauto = 'DHM_auto'                        # Let DHM run its own cycle
    comOFF = 'SYS_off'                             # Non-emergency shutdown
    
    ## Arduino command legend
    global ardTemp, ardPump, ardValve1, ardValve2, ardValve3, ardLEDready, ardLEDbusy, ardLEDbatR, ardLEDbatY, ardLEDbatG, ardALLoff
    ardTemp = "1"
    ardPump = "2"
    ardValve1 = "3"
    ardValve2 = "4"
    ardValve3 = "5"
    ardLEDready = "6"
    ardLEDbusy = "7"
    ardLEDbatR = "8"
    ardLEDbatY = "9"
    ardLEDbatG = "10"
    ardALLoff = "11"
    return
    
def touch(fname):
    times=None
    with open(fname, 'a'):
        os.utime(fname, times)
    return
