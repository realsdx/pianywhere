#!/usr/bin/env python
import socket
import fcntl
import struct
import commands as sp
import logging
import time

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
            logger.info("Device %s is up -IP %s" % (ifname,ip))
            s.close()
            return True
        else:
            s.close()
            logger.error( "Can't get the Device %s IP" % (ifname))

    except IOError as e:
        if (e.errno == 19 ):
            logger.warning("No Such device- %s" %(ifname))
            s.close()
            return "NODEV"
        if (e.errno == 99 ):
            logger.warning("Interface %s is down" %(ifname))
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

def restart_net():
    status,result = sp.getstatusoutput("sudo systemctl restart networking")
    if status == 0:
        logger.info("networking service restarted")
    else:
        logger.warning("DNT KNOW")


ppp = check('ppp0')

while(ppp == False):
    logger.warning("Interface ppp0 is down. Attempting to restart networking.service")
    restart_net()
    time.sleep(5)
    logger.info("networking.service restart done. Cheking again")
    ppp = check('ppp0')

if(ppp == True):
    logger.info("Interface ppp0 is up")
    check_net('ppp0')

if(ppp == "NODEV"):
    logger.critical("ppp0 Interface not detected.Check Serial conection. Atempting restart")
    restart_net()
    time.sleep(5)
    logger.info("networking.service restart done. Cheking again")
    ppp = check('ppp0')
