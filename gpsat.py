import serial
import time

SERIAL_PORT = "/dev/ttyUSB2"

ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=2)
ser.write(str.encode("AT\r"))
time.sleep(0.5)
reply = ser.read(ser.inWaiting())

if "OK".encode() in reply:
        print("Setup OKAY.")

        ser.write(str.encode("AT+CGPS=?\r"))
        time.sleep(0.5)
        reply = ser.read(ser.inWaiting())

        ##Parse for checking
        reply = reply.decode.split("\n")
        if reply[0].startswith("+CGPS"):
            if reply[0].split(":").[1] == "1,1":
                print("GPS ALREADY ACTIVATED")
            elif reply[0].split(":").[1] == "0,1":
                print("Activating GPS ...")
                ser.write((str.encode("AT+CGPS=1\r"))
                time.sleep(0.5)
                res = ser.read(ser.inWaiting()).decode()
                if "OK" in res:
                    print("GPS SETUP SUCCESSFULL")
                else:
                    print("GPS SETUP ERROR")
        else:
            print("GPS INIT ERROR.")



        ##=======
        # if "OK" in reply.decode():
        #     print("GPS Setup Completed")
        # print(reply.decode())

        #while True:
        ser.write(str.encode("AT+CGPSINFO\r"))
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        print(reply.decode())

else:
        print("Setup Not Complete.")

ser.close()
