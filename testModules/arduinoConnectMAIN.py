"""
This script is intended to test whether or not 'import serial' needs to be declared
in everyscript or if its ok to just declare it in one. This script will act as the main
script of the system, and call on 'arduino_connect.py' which is the routine that has
'import serial'.
"""

import arduino_connect
arduino_connect.arduino_connect()

