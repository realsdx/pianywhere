import serial
import time
import logging

SERIAL_PORT = "/dev/ttyUSB2"

logging.basicConfig(filename="GPSDeviceCheck.log",
    format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def check_gps(ser):
    ser.write(str.encode("AT+CGPS?\r"))
    time.sleep(0.5)
    reply = ser.read(ser.inWaiting())

    ##Parse for checking
    reply = reply.decode().split("\n")
    if reply[1].startswith("+CGPS"):
        if (reply[1].split(":")[1]).strip() == "1,1":
            logger.info("GPS ALREADY ACTIVATED")
            return True

        elif (reply[1].split(":")[1]).strip() == "0,1":
            logger.info("GPS is disabled. Activating GPS ...")
            ser.write((str.encode("AT+CGPS=1\r")))
            time.sleep(0.5)
            res = ser.read(ser.inWaiting()).decode()
            if "OK" in res:
                logger.info("GPS SETUP SUCCESSFULL")
                return True
            else:
                logger.error("GPS SETUP UNSUCCESSFULL")
                return False
    else:
        logger.error("GPS INITIALIZATION ERROR.")
        return False


while True:
    try:
        ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=2)
        ser.write(str.encode("AT\r"))
        time.sleep(0.5)
        reply = ser.read(ser.inWaiting())

        if "OK".encode() in reply:    
            check_gps(ser)

        else:
            logger.warning("No proper AT response.")
        ser.close()

    except Exception as e:
        logger.error(str(e))
        pass

    ## Check GPS DEVICE every 30 mins
    time.sleep(1800)
