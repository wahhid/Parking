import serial
from time import sleep

try:
    ser = serial.Serial('/dev/ttyACM1', 9600)
    print("Connected To Manless Embedeed")
    ser.write('CNS')
    while True:
        data = ser.readline()
        if len(data) > 0:
            print data.strip()
            if data.strip() == 'RT':
                ser.write('RTS')
                print("Response Request Ticket")
            if data.strip() == 'CD':
                ser.write('RCK')
                print("Response Check Device")
        sleep(0.5)    
    
    ser.close()
    
except serial.serialutil.SerialException as e:
    print(e)