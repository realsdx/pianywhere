import serial
import sys
import time

SERIAL_PORT = "/dev/ttyUSB2"

ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=5)
ser.write(str.encode("AT\r"))
time.sleep(2)
reply = ser.read(ser.inWaiting())

if "OK".encode() in reply:
    print("AT Commander is ready +++")

    while True:
        try:
            com = input("=>")
            if com:
                com = com+"\r"
                ser.write(str.encode(com))
                time.sleep(0.5)
                reply = ser.read(ser.inWaiting())
                print(reply.decode())
            else:
                print("Provide an AT comamnad")
                continue
        except KeyboardInterrupt:
            ser.close()
            print("\nClosing the Opened PORT.")
            sys.exit(1)
        except Exception as e:
            ser.close()
            sys.exit(1)
            print(e)
else:
    print("AT PORT is working properly")

ser.close()
sys.exit(0)

