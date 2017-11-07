"""

Date Created:       2017.10.09
Date Last Modified: 2017.11.03

This script is intended to check the physical buttons of the orangeBox and execute
the appropriate commands when pressed.

This script should be called from the main function as a subprocess

"""

import GET
import SET
import time
import subprocess
import kill
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
    V3   = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonV3))
    Quit = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonQuit))
    DAQ  = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonDAQ))
    
    if pump == 0:
        ## No need to check whether the sample side valves are open, the arduino does that
        header.touch(pumpLock)
        subprocess.Popen(["sudo","%s/runPump.py" % (header.codeFolder)])
        while pump == 0:
            pump = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.buttonPump))
        os.remove(pumpLock)
    
    if V1_2 == 0:
        V1 = GET.arduinoPin(header.relayV1[0])
        V2 = GET.arduinoPin(header.relayV2[0])
        ## If any of the valves are closed (on), then open them
        if (V1 == 1 or V2 == 1):
            state = ["off", "off"]
        else:
            state = ["on", "on"]
        pinNumber = [header.relayV1[0], header.relayV2[0]]
        Error = SET.arduinoRelay(pinNumber, state)
        if (True in Error):
            message = "An unknown error occured when setting valve 1 and/or 2"
            PRINT.event(message)
    
    if V3 == 0:
        V3 = GET.arduinoPin(header.relayV3[0])
        
        if V3 == 0:
            state = "on"
        else:
            state = "off"
        
        Error = SET.arduinoRelay(header.relayV3, state)
        if (True in Error):
            message = "An unknown error occured when setting valve 1 and/or 2"
            PRINT.event(message)
            
    if Quit == 0:
        kill.me("now")
    
    if DAQ == 0:
        ## Turn busy light on
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
    