import serial

SERIAL_PORT = "/dev/ttyUSB2"

ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=5)
ser.write("AT\r")
reply = ser.read(ser.inWritting())

if "OK" in reply:
	print("Setup OKAY.")

	ser.write("AT+CGPS=1\r")
	reply = ser.read(ser.inWritting())
	print(reply)
else:
	print("Setup Not Complete.")

