import serial
import time
import pynmea2
import json
import logging

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from mods.firesync import FirebaseDB

PORT="/dev/ttyUSB1"

logging.basicConfig(filename="nmea-sync.log",
    format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

##Firebase DB setup
fdb = FirebaseDB()
model = fdb.new_model("NMEA")

def upload_to_firebase(data):
    """Converts a python dict object and uploads it to Firebase database"""
    data = json.dumps(data)
    fdb.push_new(model,data)

try:
    ser = serial.Serial(PORT,baudrate=9600, timeout=1)
    logger.info("Serial %s is connected successfully"%PORT)
    time.sleep(0.5)

    while True:
        reply = ser.read(ser.inWaiting())
        reply = reply.decode(errors='replace').split("\n")

        gp=""
        for line in reply:
            if "$GPGGA" in line:
                gp=line

        if gp:
            nmeaobj = pynmea2.parse(gp)
            data = {nmeaobj.fields[i][0] : nmeaobj.data[i] for i in range(len(nmeaobj.fields))}
            upload_to_firebase(data)
            logger.info("GPS:GPGGA data successfully uploaded to FIrebase")
        else:
            logger.warning("No GPS:GPGGA data recevied")

        time.sleep(60)

except Exception as e:
    ser.close()
    logger.error(e.strerror)


ser.close()

