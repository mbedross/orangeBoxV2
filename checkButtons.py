"""

Date Created:       2017.10.09
Date Last Modified: 2017.10.09

This script is intended to check the physical buttons of the orangeBox and execute
the appropriate commands when pressed.

This script should be called from the main function as a subprocess

"""

import RUN
import SET
import time
import header
header.init()

## Turn GPIO pins for buttons on
os.system('echo 1 > /sys/class/gpio/gpio%d/value' %(header.buttonPump))
os.system('echo 1 > /sys/class/gpio/gpio%d/value' %(header.buttonV1_2))
os.system('echo 1 > /sys/class/gpio/gpio%d/value' %(header.buttonV3))
os.system('echo 1 > /sys/class/gpio/gpio%d/value' %(header.buttonQuit))
os.system('echo 1 > /sys/class/gpio/gpio%d/value' %(header.buttonDAQ))

while True:
    ## Begin checking buttons. These buttons should be normally HIGH (LOW if pushed)
    pump = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonPump))
    V1_2 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonV1_2))
    V3 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonV3))
    Quit = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonQuit))
    DAQ = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonDAQ))
    
    if pump == 0:
        header.touch(pumpLock)
        RUN.pump()
        while pump == 0:
            pump = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonPump))
        os.remove(pumpLock)
    
    if V1_2 == 0:
        ## Check current status of the two valves
        V1 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.valve1))
        V2 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.valve2))
        
        if (V1 == 0 or V2 == 0):
            vNumber = [header.valve1, header.valve2]
            SET.valve(vNumber, 1)
        else:
            vNumber = [header.valve1, header.valve2]
            SET.valve(vNumber, 0)
    
    if V3 ==0:
        V3 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.valve3))
        
        if V3 == 0:
            SET.valve(header.valve3, 1)
        else:
            SET.valve(header.valve3, 0)
    if Quit == 0:
        RUN.powerOFF()
    
    if DAQ == 0:
        time.sleep(2)
        vid = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonDAQ))
        if vid == 0:
            """
            TO BE WRITTEN!!!
            
            If vid == 0 then the button has been pushed for more than two seconds.
            This means user wants a video recording so run video DAQ sequence.
            """
        else:
            """
            TO BE WRITTEN!!!
            
            If vid == 1 then the button was NOT pushed for more than two seconds.
            THis means user wants a snapshot recording so run snapshot DAQ
            """
    