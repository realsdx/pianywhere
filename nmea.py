import serial
import time
import pynmea2
from firesync import FirebaseDB
import json

PORT="/dev/ttyUSB1"
ser = serial.Serial(PORT,baudrate=9600, timeout=1)
time.sleep(0.5)

##Firebase DB setup
fdb = FirebaseDB()
model = fdb.new_model("NMEA")

reply = ser.read(ser.inWaiting())
reply = reply.decode(errors='replace').split("\n")

gp=""
for line in reply:
    if "$GPGGA" in line:
        gp=line
       # print("GP:", gp)
if gp:
    nmeaobj = pynmea2.parse(gp)
    data = {nmeaobj.fields[i][0] : nmeaobj.data[i] for i in range(len(nmeaobj.fields))}
    data = json.dumps(data)
    fdb.push_new(model,data)
    print(data)
else:
    print("No data recevied")



ser.close()

