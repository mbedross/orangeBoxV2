"""
Date Created:       2017.09.11
Date Last Modified: 2017.09.11

This script contains modules that will print a message to the appropriate event
log

"""

import GET
import sock
import header
header.init()

def event(message):
    Message = "- ", message
    (st,ts) = GET.time_stamp()
    file = open('%s/EventLog.txt' % (header.filefolder), "a")
    print >>file, st, Message
    file.close
    return

def emergency(message):
    Message = "- ", message
    (st,ts) = GET.time_stamp()
    file = open('%s/EmergencyLog.txt' % (header.filefolder), "a")
    print >>file, st, Message
    file.close
    sock.sendto(Message, (header.UDP_IP, header.UDP_PORT))
    return

def udp(message):
    Message = "- ", message
    (st,ts) = GET.time_stamp()
    sock.sendto(Message, (header.UDP_IP, header.UDP_PORT))
    return