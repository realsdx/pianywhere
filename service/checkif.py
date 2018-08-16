#!/usr/bin/env python
import socket
import fcntl
import struct
import commands as sp
import logging

logging.basicConfig(filename="InterfaceCheck.log",
    format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def check(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip=socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),0x8915,
            struct.pack('256s', ifname[:15]))[20:24])
        if ip:
            logger.info( "Device is up -IP %s" % ip)
            s.close()
            return True
        else:
            s.close()
            logger.error( "Can't get the Device IP")

    except IOError as e:
        if (e.errno == 19 ):
            logger.warning("No Such device")
            s.close()
            return False
        if (e.errno == 99 ):
            logger.warning("Interface is down")
            s.close()
            return False
        else:
            logger.error(e.strerror)
            s.close()

def check_net(ifname):
    try:
        status,result = sp.getstatusoutput("ping -c1 -w2 -I " + str(ifname)+ " 8.8.8.8")
        if status == 0:
            logger.info("Interface %s has a working internet." %(ifname))
            return True
        else:
            logger.warning("Interface %s has no internet" %(ifname))
            return False
    except Exception as e:
        logger.error(e.strerror)

check_net('eno12')
check('eno12')
check('eno1')
check('wlo1')
    
