# orangeBoxV2

This repository is for the operating software of the 2nd generation DHM field instrument built by Catech/JPL/PDX.

## Getting Started

The operating software is written exclusively in Python 2.7. Most of the modules used are standard modules that are included in standard python distributions, with the exception of a few, which will be discussed.

### Prerequisites

#### Hardware

This software was written specifically to run on an [UDOO x86 Ultra](https://www.udoo.org/udoo-x86/).

A custom PCB is necessary to interface the UDOO with all peripheral devices of the instrument. These devices include:

* [Laser driver](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=1364)
* [Microfluidic pump](http://www.theleeco.com/whats-new/lpm-inert-solenoid-pump.cfm)
* [Microfluidic valves](http://www.theleeco.com/electro-fluidic-systems/solenoid-valves/lhl/lhl-series-solenoid-valves.cfm)
* [TEC temperature controllers](http://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=241420187&uq=636439335205899036)
* [Thermistors](https://www.digikey.com/product-detail/en/cantherm/MF52A2103J3470/317-1258-ND/1191033)
* Moisture sensors
* [LED's](https://www.digikey.com/product-detail/en/visual-communications-company-vcc/L65DR2L/L65DR2L-ND/6166297)
* User input buttons

Please contact mbedross@caltech.edu for a full list of needed parts and custom PCB specifications

#### Software

The operating software is written exclusively in Python 2.7 with mostly standard modules that are included in standard python distributions

There are however some modules used in this OS that require installation. These modules are:

* [ntplib](https://pypi.python.org/pypi/ntplib/)

### Installing

With python and the necessary modules installed, clone this repository into a directory on the x86 with admin privileges.

Add the '__init__.py' code as cronjob to run at start up.

## Understanding the code

The code is written with a single header file that establishes all global variables as well as GPIO pin numbers.

All 'nomenclature' is located in this file.

The subroutines of the instrument are then split into multiple python scripts.

### RUN.py

This script contains all modules that run a function. The modules include:

```
RUN.pump()
RUN.connectUDP()
RUN.powerOFF()
RUN.EMERGENCYoff()
```

These modules require no inputs.

#### RUN.pump()

When calling RUN.pump() a pump lock file must also be created by the script that calls the pump command. RUN.pump() will run the pump for however long the lock file exists. See example below:

```
import os
import RUN
import header

header.init()

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)
    return

touch(header.pumpLock)         ## Create lock file
RUN.pump()
os.remove(header.pumpLock)     ## Remove lock file
```

#### RUN.connectUDP()

This script attempts to connect to an IP address and Port Number defined in the header.py file. The IP and Port numbers are defined as the variable:

```
header.UDP_IP
header.UDP_PORT
```

Once connected, the script will send a message to the host UDP server to confirm connection, this message is also defined in the header.py file as header.MESSAGE

#### RUN.powerOFF()

This shuts down the instrument in a routine way. (non-emergency shut down). See the module for more detail but this ends all subprocesses, makes sure all peripheral devices are off (laser, pump, valves, etc.), and sends a confirmation message via UDP that shut down is occurring. It then waits 5 seconds before shutting itself down.

#### RUN.EMERGENCYoff()

This is to be called in emergency situations. This does not wait for programs to quit nor does it go through regular shut down procedures like making sure the valves and laser are off.

### GET.py

This script contains all modules that query the status of an operation. The modules include:

```
GET.relay(relayNumber)
GET.pump()
GET.temp()
```

#### GET.relay(relayNumber)

This module returns a logical value as to whether a relay coil is energized or not. The relays are Normally Open (NO) and control peripheral devices. See header.py for a list of relay variables.

#### GET.pump()

This module checks if the pump lock file exists (header.pumpLock). If the file exists, then the pump is on.

#### GET.temp()

This module checks the temperatures of the five thermistors on the instrument and returns their values (in degC) as an array.

### SET.py

This script contains all modules that set the status of an operation. The modules include:

```
SET.LED(pinNumber, state)
SET.valve(vNumber, state)
SET.DAQtime(daqTime)
SET.powerRelay(relayNumber, state)
```

#### SET.LED(pinNumber, state)

This module is used to turn LED's on and off. For the pump and valves of the instrument, this isn't necessary. The LED's for those components are physically wired with the relay that controls them so the LED will always turn on when its respective device is on.

Input variables include the LED pin number (see header.py) and desired state. state = 1 -> ON and state = 0 -> OFF

#### SET.valve(vNumber, state)

This module energizes or de-energizes the relay that controls the microfluidic valves. These valves are Normally Open (NO) and so energizing the coils (state = 1) will CLOSE the valve. vNumber is the valve relay pin number (see header.py)

#### SET.DAQtime(daqTime)

This module sets the length of time that DAQ will occur. The camera is controlled by a lock file so this module changes the time variable that is used to touch and remove the camera lock file.

#### SET.powerRelay(relayNumber, state)

This module energizes or de-energizes relay coils. These relays are Single Pole Dual Throw (SPDT). There is one common, one Normally Open (NO), and one Normally Closed (NC) lead. Energizing the coil (state = 1) completes the circuit between the common and NC lead.
