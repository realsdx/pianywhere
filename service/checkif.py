#!/usr/bin/env python
import socket
import fcntl
import struct
import commands as sp

def check(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip=socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),0x8915,
            struct.pack('256s', ifname[:15]))[20:24])
        if ip:
            print "Device is up -IP %s" % ip
            s.close()
            return True
        else:
            s.close()
            print "Can't get the Device IP"

    except IOError as e:
        if (e.errno == 19 ):
            print "No Such device"
            s.close()
            return False
        if (e.errno == 99 ):
            print "Interface is down"
            s.close()
            return False
        else:
            print e
            s.close()

def check_net(ifname):
    status,result = sp.getstatusoutput("ping -c1 -w2 -I " + str(ifname)+ " 8.8.8.8")
    if status == 0:
        print("TRUE")
        return True
    else:
        print("System  is DOWN !")
        return False

check_net('wlo1')
    
