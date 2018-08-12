import serial
import time
import pynmea2

PORT="/dev/ttyUSB1"
ser = serial.Serial(PORT,baudrate=9600, timeout=1)
time.sleep(0.5)
reply = ser.read(ser.inWaiting())
reply = reply.decode(errors='replace').split("\n")

gp=""
for line in reply:
    if "$GPGGA" in line:
        gp=line
        print("GP:", gp)

nmeaobj = pynmea2.parse(gp)

table=['%s: %s' % (nmeaobj.fields[i][0], nmeaobj.data[i]) 
             for i in range(len(nmeaobj.fields))]
print(table)



ser.close()

