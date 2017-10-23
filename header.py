"""
Date Created:       2016.04.06
Date Last Modified: 2017.09.11
Author: Manuel Bedrossian

This is a header file for the operating system for the 2nd Gen. orangeBox DHM field
instrument. All global variables should be defined here to be used throughout all
dependent code.

Manu's MacBook Pro's IP in the wind tunnel is 192.168.1.14 (port is arbitrary)

"""

import ntplib
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
    ## Relays
    global relayLaser, relayPump, relayValve1, relayValve2, relayValve3, relayTEC1, relayTEC2, relay2, relay3
    relayLaser = 346
    relayPump = 6
    relayValve1 = 5
    relayValve2 = 4
    relayValve3 = 3
    relayTEC1 = 344
    relayTEC2 = 351
    relay2 = 499
    relay3 = 497
    relayALL = [relayLaser, relayPump, relayValve1, relayValve2, relayValve3, relayTEC1, relayTEC2, relay2, relay3]
    
    global laser, moistPower, moist1, moist2, moist3, moist4, temp1, temp2, temp3, temp4, batteryV, shuntV,diodeC
    laser = 1
    moistPower = 330                 ## GPIO moisture sensor power
    moist1 = 329                     ## GPIO moisture sensor 1
    moist2 = 332                     ## GPIO moisture sensor 2
    moist3 = 333                     ## GPIO moisture sensor 3
    moist4 = 336                     ## GPIO moisture sensor 4
    tempPower = 2
    #temp1 =  [0, 4]                  ## [adcBank, pin] - temp sensor 1
    #temp2 =  [0, 5]                  ## [adcBank, pin] - temp sensor 2
    #temp3 =  [1, 0]                  ## [adcBank, pin] - temp sensor 3
    #temp4 =  [1, 1]                  ## [adcBank, pin] - temp sensor 4
    #tempSC = [1, 2]                  ## [adcBank, pin] - temp sensor SC
    #batteryV = 1                     ## ADC for battery voltage
    #shuntV = 1                       ## ADC pin for system power shunt
    #diodeC = 1                       ## Arduino ADC pin for laser diode current
    
    
    ## Define file to read for temp pins as analog inputs
    #temp1 =  '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(temp1[0], temp1[1])
    #temp2 =  '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(temp2[0], temp2[1])
    #temp3 =  '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(temp3[0], temp3[1])
    #temp4 =  '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(temp4[0], temp4[1])
    #tempSC = '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(tempSC[0], tempSC[1])
    
    ## GPIO pins for status LED's
    global LEDbatG, LEDbatY, LEDbatR, LEDbusy, LEDready, LEDpump, LEDv1, LEDv2, LEDv3
    LEDbatG = 11
    LEDbatY = 10
    LEDbatR = 9
    LEDbusy = 8
    LEDready = 7
    LEDpump = 6                      ## Same GPIO pin as relayPump
    LEDv1 = 5                        ## Same GPIO pin as relayV1
    LEDv2 = 4                        ## Same GPIO pin as relayV2
    LEDv3 = 3                        ## Same GPIO pin as relayV3
    
    ## GPIO pins for push buttons
    global buttonPump, buttonV1_2, buttonV3, buttonQuit, buttonDAQ
    buttonPump = 326
    buttonV1_2 = 347
    buttonV3 = 349
    buttonQuit = 350
    buttonDAQ = 366
    
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
    global pumpTime, DAQtime, ADC, UDP_IP, UDP_PORT, MESSAGE, tempA, tempB, tempC, Rtemp, Temp, Rshunt, batCap, connected
    pumpTime = 10                      ## Pump time to cycle in new sample
    DAQtime = 15                       ## Standard image acq. time in seconds
    ADC = 24
    UDP_IP = "192.168.1.14"            ## IP address to host computer
    UDP_PORT = 5005                    ## UDP Port # to host computer
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
    
    ## UDP message legend
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
    
def defineGPIO():
    ## Export all GPIO pins so that they are available for access
    
    
    ## Establish all LED pins as GPIO outputs
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(LEDbatG))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(LEDbatY))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(LEDbatR))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(LEDbusy))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(LEDready))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(LEDpump))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(LEDv1))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(LEDv2))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(LEDv3))
    
    ## Establish all push buttons as GPIO inputs
    os.system('echo in > /sys/class/gpio/gpio%d/direction' %(buttonPump))
    os.system('echo in > /sys/class/gpio/gpio%d/direction' %(buttonV1_2))
    os.system('echo in > /sys/class/gpio/gpio%d/direction' %(buttonV3))
    os.system('echo in > /sys/class/gpio/gpio%d/direction' %(buttonQuit))
    os.system('echo in > /sys/class/gpio/gpio%d/direction' %(buttonDAQ))
    
    ## Establish all moisture sensor pins as GPIO inputs and the power pin as output
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(moistPower))
    os.system('echo in > /sys/class/gpio/gpio%d/direction' %(moist1))
    os.system('echo in > /sys/class/gpio/gpio%d/direction' %(moist2))
    os.system('echo in > /sys/class/gpio/gpio%d/direction' %(moist3))
    os.system('echo in > /sys/class/gpio/gpio%d/direction' %(moist4))
    
    ## Establish remaining GPIO pins as appropriate
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(laser))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(relayLaser))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(relayPump))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(relayValve1))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(relayValve2))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(relayValve3))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(relayTEC1))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(relayTEC2))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(relay2))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(relay3))
    return

def syncTime():
    try:
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org')
        os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
        message = "Time syncronized with host server"
        PRINT.event(message)
    except Exception as e:
        message = "Could not sync time with host server. Error is as follows:\n", e
        PRINT.event(message)
    return
    
def touch(fname):
    times=None
    with open(fname, 'a'):
        os.utime(fname, times)
    return
