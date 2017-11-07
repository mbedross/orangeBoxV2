"""
This script is intended to kill (shut down) the orangeBoxV2
"""

import SET
import PRINT
import os
import time
import header
header.init()

def laser():
    """
    IMPORTANT!!!
    
    This code is TENTATIVE. Must first test if PWM is valid with the laser driver
    If not, ramping is not possible, must design a voltage divider such that the
    max output of the GPIO (1.8V) gives the desired optical power desired
    """
    t_ramp = 5  ## Time in seconds to ramp up laser
    v_now=0.394
    v_low = 0
    for t in range(0,t_ramp):
        v_new = v_now-v_high/t_ramp
        os.system('/home/shamu/mcc-libhid/write_DtoA_channel 0 %f' % (v_new))
        v_now = v_new
        time.sleep(1)
    message = "Laser finished ramping DOWN and is OFF"
    PRINT.event(message)
    return

def me(when):
    ## Ramp down laser
    laser()
    ## Make sure all valves and power relays are off (valves are normally open)
    SET.relay(header.relayUDOO, header.relayUDOOoff)
    SET.arduinoRelay(header.relayArduino, header.relayArduinoOff)
    __init__.unexportGPIO(header.GPIO)
    message = "Non-emergency shut down"
    PRINT.event(message)
    if (when != "now"):
        time.sleep(when)
    # Shut down
    os.system('shutdown -P now')
    return

def EMERGENCY():
    ## This call is similiar to a hard power off, it doesnt wait for current programs
    ## to end or to unmount any drives, it immediately calls for a reboot (but
    ## remain powered off)
    PRINT.emergency('Emergency shut off now!, look at previous event for error details.')
    os.system('echo 1 > /proc/sys/kernel/sysrq && echo b > /proc/sysrq-trigger')
    return