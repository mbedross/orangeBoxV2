"""
Created on 2015.10.07

@author: manu
"""

import serial
import time
import datetime
import os

## Open serial port, ser = Arduino, ser1 = cam/laser relay board
ser = serial.Serial("/dev/ttyACM1", baudrate = 9600)
ser1 = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=10)
time.sleep(.5)

## open serial ports if closed
if(ser.isOpen() == False):
    ser.open()
if(ser1.isOpen() == False):
    ser1.open()


## Define constants


## filefolder is the directory where the holograms will be store in timestamped subdirectories
filefolder = '/home/shamu/Desktop/Sample Chamber Loading'

## Specify Event Log output file
file = open('%s/EventLog.txt' % (filefolder), "a")

v_high = 0.394        ## Desired Laser Voltage
t_ramp = 5            ## Desired Laser Ramp time [s]

## Lines 8-15 can be automated later with moisture level sensors
volume = raw_input("Approximately how much sample is there? [in mL] ")
pvol = raw_input("What volume per pump cycle would you like? [in mL/cycle] Enter SC for one sample chamber volume ")
if pvol == "SC":
    ptime = 0.375
    maxiter = int(volume)/ 0.025
else:
    ptime = int(pvol) / 0.06667           ## flowrate of 0.067 mL/s
    maxiter = int(volume) / int(pvol)     ## Max cycle count


    
def ramp_laser(v_high,t_ramp, file):
    v_now=0
    for t in range(0,t_ramp):
        v_new = v_now+v_high/5
        os.system('/home/shamu/mcc-libhid/write_DtoA_channel 0 %f' % (v_new))
        v_now = v_new
        time.sleep(1)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print >>file, st, " - Laser finished ramping up and is ON"
    return
def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)
    return
def arduino_connect(file):
    
    connected = False;        ##(this is a logical statement to make connection
    while not connected:
        serin = ser.read()
        connected = True
        ts = time.time()
    	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print >>file, st, " - Arduino Connected"
    return
def runcamera(file, filefolder):
    Holo = 'Holograms'
    camtime=2
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if not os.path.exists('%s/%s' % (filefolder, st)):
        os.makedirs('%s/%s' % (filefolder, st),0755)
        os.makedirs('%s/%s/%s' % (filefolder, st, Holo),0755)
    os.chdir('%s/%s' % (filefolder, st))
    ## open('/home/shamu/Desktop/Sample Chamber Loading/%s/Holograms/timestamps.txt' % (st),'a')

    touch('/tmp/.vmbcamlock')
    os.system("/home/shamu/Downloads/Vimba_1_3/VimbaC/Examples/AsynchronousGrab/Build/Make/binary/x86_64bit/AsynchronousGrab >timestamps.txt &")
    time.sleep(camtime+1)       ## add one second because there is a second of overhead before recording
    os.remove('/tmp/.vmbcamlock')

    time.sleep(1)
    ts2 = time.time()
    st2 = datetime.datetime.fromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
    print >>file, st2, " - recorded to %s/%s/Holograms for " % (filefolder, st), camtime," seconds"
    return
   
def sc_loop(ptime,maxiter, file):
    
    iter = 1              ## Initialize cycle count
    totalvol = 0
    cyclevol = 0
    while iter < maxiter:
        ts = time.time()
    	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print >>file, st, " - pump cycle #", iter
        ## Tell the arduino to begin pumping
        ser.write("1".encode())
        pump = ser.readline()
        if pump == 'P':
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print >>file, st, " - Sample chamber pump turned ON"
        ts = time.time()
    	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print >>file, st, " - Sample chamber pump turned ON"
        time.sleep(ptime)
        ser.write("2".encode())
        ts2 = time.time()
    	st2 = datetime.datetime.fromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
        print >>file, st2, " - Sample Chamber Pump turned OFF"
        print >>file, st2, " - Pump was on for",ts2-ts, "seconds"
        cyclevol = 0.0667*(ts2-ts)
        print >>file, st2, " - ", cyclevol," mL of sample were pumped this cycle"
        totalvol = totalvol+cyclevol
        print >>file, st2, " - ", totalvol, " mL of sample have been pumped so far"
        time.sleep(3)
        runcamera(file) ## Run camera
        ## imaged = raw_input("Sample is ready for imaging [Press any key once imaged] ")
        iter = iter+1
    return

## Turn Camera on and ramp laser
## Make sure laser is off at DtoA Board

os.system('/home/shamu/mcc-libhid/write_DtoA_channel 0 0')
ser1.write("RELS.ON\x0D\x0A")
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print >>file, st, " - Camera turned ON"
print >>file, st, " - Laser began ramping up"
ramp_laser(v_high,t_ramp)
time.sleep(15)

## Connect to Arduino
arduino_connect(file)

## Run imaging loop
sc_loop(ptime,maxiter, file)

os.system('/home/shamu/mcc-libhid/write_DtoA_channel 0 0')
ser1.write("RELS.OFF\x0D\x0A")
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print >>file, st, " - Camera turned OFF"
print >>file, st, " - Laser turned OFF"
ser.close()
ser1.close()