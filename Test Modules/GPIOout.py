import sys
import time
## filePath should be a string specifying where the code is to be tested
filePath = '/Users/manuelbedrossian/NetBeansProjects/orangeboxv2/orangeboxv2'
sys.path.append(filePath)

import header
header.init()

header.defineGPIO()

## pin2Test is the variable that defines the GPIO pin to be tested
pin2Test = header.relayPump

os.system('echo "1" |sudo tee /sys/class/gpio/gpio%s/value' %(pin2Test))
time.sleep(5)
os.system('echo "0" |sudo tee /sys/class/gpio/gpio%s/value' %(pin2Test))