import serial
import time

SERIAL_PORT = "/dev/ttyUSB2"

ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=5)
ser.write(str.encode("AT\r"))
time.sleep(2)
reply = ser.read(ser.inWaiting())

if "OK".encode() in reply:
        print("Setup OKAY.")

        ser.write(str.encode("AT+CGPS=?\r"))
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        if "OK" in reply.decode():
            print("GPS Setup Completed")
        print(reply.decode())

        #while True:
        ser.write(str.encode("AT+CGPSINFO\r"))
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        print(reply.decode())

else:
        print("Setup Not Complete.")

ser.close()
