"""

Date Created:       2017.09.16
Date Last Modified: 2017.09.18

This script is for the sole purpose of monitoring the moisture sensors in the
instrument. If at anytime, the moisture sensors fault (sense water), the emergency
power off function (RUN.EMERGENCYoff()) is called to immediately shut down the system

This script should be called as a subprocess by the main python function

"""

import kill
import PRINT
import os
import time
import header
header.init()

while True:
    ## Begin checking moisture sensors every second
    os.system('echo 1 > /sys/class/gpio/gpio%d/value' %(header.moistPower))
    time.sleep(0.5)       ## Accounting for overhead to turn on moisture sensors
    header.statusM1 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.moist1))
    header.statusM2 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.moist2))
    header.statusM3 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.moist3))
    header.statusM4 = os.system('cat |sudo tee /sys/class/gpio/gpio%s/value' %(header.moist4))
    os.system('echo 0 > /sys/class/gpio/gpio%d/value' %(header.moistPower))
    if (
            header.moist1 == 1 or header.moist2 == 1 or
            header.moist3 == 1 or header.moist4 == 1
        ):
        message = "Moisture detected. Sensor statuses are: %d, %d, %d, %d emergency shut off now" %(header.statusM1, header.statusM2, statusM3, header.statusM4)
        PRINT.emergency(message)
        kill.EMERGENCY()
    time.sleep(1)