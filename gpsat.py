import serial
import time

SERIAL_PORT = "/dev/ttyUSB2"

ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=5)
ser.write(str.encode("AT\r"))
time.sleep(2)
reply = ser.read(ser.inWaiting())

if "OK".encode() in reply:
	print("Setup OKAY.")

	ser.write(str.encode("AT+CGPS=1\r"))
	time.sleep(2)
	reply = ser.read(ser.inWaiting())
	print(reply.decode())
	ser.write(str.encode("AT+CGPSINFO\r"))
	time.sleep(2)
	reply = ser.read(ser.inWaiting())
	print(reply.decode())

else:
	print("Setup Not Complete.")

