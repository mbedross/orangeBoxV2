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
    global filefolder, codefolder, GPIOfolder, pumpLock, camLock
    ## Identify eventlog directory
    filefolder = '/home/odroid/Desktop/BRUIEdhm_os/EventLog'
    ## Identify subroutine direcotry
    codefolder = '/home/odroid/Desktop/BRUIEdhm_os/FINAL'
    ## Identify folder for GPIO files
    GPIOfolder = '/usr/bin'
    ## Hardware lock files
    pumpLock = '/home/odroid/Desktop/BRUIEdhm_os/pumpLock.tmp'
    camLock = '/home/odroid/Desktop/BRUIEdhm_os/camLock.tmp'
    
    ## GPIO Pin export numbers
    global laserPower, pumpRelay, EMsc, laserRelay, valve1, valve2, valve3, moist1, moist2, moist3, moist4, temp1, temp2, temp3, temp4, batteryV, shuntV
    laserPower = 33                  ## GPIO pin number - Laser optical power
    pumpRelay = 24                   ## GPIO pin number - Pump power relay
    laserRelay = 23                  ## GPIO pin number - Laser exc. power relay
    valve1 = 1                       ## GPIO pin number - Valve 1 relay
    valve2 = 2                       ## GPIO pin number - Valve 2 relay
    valve3 = 3                       ## GPIO pin number - Valve 3 relay
    moistPower = 1                   ## GPIO moisture sensor power
    moist1 = 1                       ## GPIO moisture sensor 1
    moist2 = 2                       ## GPIO moisture sensor 2
    moist3 = 3                       ## GPIO moisture sensor 3
    moist4 = 4                       ## GPIO moisture sensor 4
    temp1 =  [0, 4]                  ## [adcBank, pin] - temp sensor 1
    temp2 =  [0, 5]                  ## [adcBank, pin] - temp sensor 2
    temp3 =  [1, 0]                  ## [adcBank, pin] - temp sensor 3
    temp4 =  [1, 1]                  ## [adcBank, pin] - temp sensor 4
    tempSC = [1, 2]                  ## [adcBank, pin] - temp sensor SC
    batteryV = 1
    shuntV = 1
    
    
## Define file to read for temp pins as analog inputs
    temp1 =  '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(temp1[0], temp1[1])
    temp2 =  '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(temp2[0], temp2[1])
    temp3 =  '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(temp3[0], temp3[1])
    temp4 =  '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(temp4[0], temp4[1])
    tempSC = '/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' %(tempSC[0], tempSC[1])
    
    ## GPIO pins for status LED's
    global LEDbatG, LEDbatY, LEDbatR, LEDbusy, LEDready, LEDpump, LEDv1, LEDv2, LEDv3
    LEDbatG = 1
    LEDbatY = 2
    LEDbatR = 3
    LEDbusy = 4
    LEDready = 5
    LEDpump = 6
    LEDv1 = 7
    LEDv2 = 8
    LEDv3 = 9
    
    ## GPIO pins for push buttons
    global buttonPump, buttonV1_2, buttonV3, buttonQuit, buttonDAQ
    buttonPump = 1
    buttonV1_2 = 2
    buttonV3 = 3
    buttonQuit = 4
    buttonDAQ = 5
    
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
    global pumpTime, DAQtime, ADC, UDP_IP, UDP_PORT, MESSAGE, tempA, tempB, tempC, Rtemp, Temp, Rshunt, batCap
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
    
def defineGPIO():
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
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(laserPower))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(laserRelay))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(pumpRelay))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(valve1))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(valve2))
    os.system('echo out > /sys/class/gpio/gpio%d/direction' %(valve3))
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
    
    def touch(fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)
        return