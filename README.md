# holOS

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

### header.py

The code is written with a single header file that establishes all global variables as well as GPIO pin numbers.

All 'nomenclature' is located in this file. Below is legend of all variable names, syntax, and descriptions.

#### File Paths

Syntax: 'path/goes/here'

`fileFolder =' file path to where event log information will be stored

`codeFolder =' file path to parent directory containing holOS source code

`pumpLock =' file path to the pump lock file. This file is used as a terminator to shut the pump off.

`camLock =' file path to the camera lock file. This file is used as a terminator to stop image acquisition.

#### UDOO GPIO Pins

Syntax: [pinNumber, type]
pinNumber = integer value of the GPIO pin number
type = integer value of whether it is an input (1) or output (0)
NOTE: If adding a new GPIO pin, or deleting an existing one. Be sure that change is reflected in the variable 

`relayLaser =` relay for laser excitation voltage

`relayTEC1 =`  relay for TEC 1 (Peltier cooler)

`relayTEC2 =`  relay for TEC 2 (Peltier cooler)

`relay2 =`     general purpose relay (unused)

`relay3 =`     general purpose relay (unused)

`moistPower =` excitation voltage source for all moisture sensors

`moist1 =`     signal for moisture sensor 1

`moist2 =`     signal for moisture sensor 2

`moist3 =`     signal for moisture sensor 3

`moist4 =`     signal for moisture sensor 4

`buttonPump =` signal for 'pump' button

`buttonV1_2 =` signal for 'valve 1 and 2' button (sample side valves)

`buttonV3 =`   signal for 'valve 3' button (reference side valve)

`buttonQuit =` signal for 'quit' button

`buttonDAQ =`  signal for 'DAQ' button

`GPIO =` a list of all the above GPIO variables. This is used when the instrument initializes. All GPIO's must be 'exported' and 'defined' as either inputs or outputs. This variable makes exporting and defining simple.

#### Arduino Analog Pins

Syntax: pinNumber (without an 'A' in front)

`tempSC =` temperature sensor for the sample chamber

`temp1 =`  general purpose temperature sensor (when assembling the instrument. Make note of which sensor is where)

`temp2 =`  general purpose temperature sensor (when assembling the instrument. Make note of which sensor is where)

`temp3 =`  general purpose temperature sensor (when assembling the instrument. Make note of which sensor is where)

`temp4 =`  general purpose temperature sensor (when assembling the instrument. Make note of which sensor is where)

`diodeC =` laser diode current monitor

#### Arduino Digital Pins

Syntax: [pinNumber, state]
pinNumber = integer value of the Digital pin number
type = integer value of whether it is an on (1) or off (0) [might be deleted]

`tempPower =` excitation voltage source for all temperature sensors

`relayPump =` relay for pump and LED indicator

`relayV1 =`   relay for valve 1 and LED indicator

`relayV2 =`   relay for valve 2 and LED indicator

`relayV3 =`   relay for valve 3 and LED indicator

`LEDready =`  Green 'ready' LED indicator

`LEDbusy =`   Red 'busy' LED indicator

`LEDbatR =`   Red 'low battery' LED indicator

`LEDbatY =`   Yellow 'medium battery' indicator

`LEDbatG =`   Green 'full battery' indicator

`LEDall =`    list variable of all LED pin numbers to make flashing LED's easier

`LEDoff =`    When flashing LED's the routine expects a `state` input variable of the same size as the `pinNumber` input variable. This establishes it. See `SET.LED(pinNumber, state)`

`LEDon =`     When flashing LED's the routine expects a `state` input variable of the same size as the `pinNumber` input variable. This establishes it. See `SET.LED(pinNumber, state)`

The subroutines of the instrument are then split into multiple python scripts.

### RUN.py

This script contains all modules that run a function. The modules include:

```python
RUN.pump()
RUN.powerOFF()
RUN.EMERGENCYoff()
```

These modules require no inputs.

#### RUN.pump()

When calling RUN.pump() a pump lock file must also be created by the script that calls the pump command. RUN.pump() will run the pump for however long the lock file exists. See example below:

```python
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

#### RUN.powerOFF()

This shuts down the instrument in a routine way. (non-emergency shut down). See the module for more detail but this ends all subprocesses, makes sure all peripheral devices are off (laser, pump, valves, etc.), and sends a confirmation message via UDP that shut down is occurring. It then waits 5 seconds before shutting itself down.

#### RUN.EMERGENCYoff()

This is to be called in emergency situations. This does not wait for programs to quit nor does it go through regular shut down procedures like making sure the valves and laser are off.

### GET.py

This script contains all modules that query the status of an operation. The modules include:

```python
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

These thermistors have a nominal resistance of 10 kOhms at 25 degrees C. To calculate temperature from these Negative Temperature Correlation (NTC) thermistors, the simplified Steinhart-Hart Equation is used. The Beta value for the thermistors used in the instrument is 3470.

### SET.py

This script contains all modules that set the status of an operation. The modules include:

```python
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

### MAIN.py

#### MAIN.connectUDP()

This script attempts to connect to an IP address and Port Number defined in the header.py file. The IP and Port numbers are defined as the variable:

```python
header.UDP_IP
header.UDP_PORT
```

Once connected, the script will send a message to the host UDP server to confirm connection, this message is also defined in the header.py file as header.MESSAGE
