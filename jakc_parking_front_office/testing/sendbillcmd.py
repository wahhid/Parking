import serial
from time import sleep

line = []

try:
    ser = serial.Serial('/dev/ttyACM0', 9600, bytesize=8, rtscts=0)
    print("Connected Bill Acceptor")
    print("Send Command")
    #Send Hex
    thestring = "\x02\x08\x10\x1F\x10\x00\x03\x17"        
    ser.write(thestring)
    
    #Send Integer
    #ser.write('3')
    #ser.write('0')
    #ser.write('1')
    #ser.write('254')    
    #ser.write('254')

    sleep(0.5)    
    print("Waiting Response")
    while True:
        #print "--------------------------------"        
        data = ser.read(1)
        print data.encode('hex')        
        #response = struct.unpack("!b", data)
        #print response
        #print "--------------------------------"                
        #print data.strip().decode('hex')    
    #while True:
    #    data = ser.read() 
    #    line.append(data)       
    #    print str(line)    
    #print("Send Data")
    #ser.write('0x02')
    #ser.write('0x08')
    #ser.write('0x10')
    #ser.write('0x1F')    
    ##ser.write('0x00')
    #ser.write('0x03')
    #ser.write('0x17')
     
    #thestring = "\x02\x08\x11\x1F\x10\x00\x03\x16"        
    #ser.write(thestring)
    #sleep(0.5)
    #print(thestring)
    #print("End Data")
    
    #while True:
    #    data = ser.read()        
    #    line.append(data)
    #    print str(line)       
    
    ser.close()
    print("Disconnected Bill Acceptor")
except serial.serialutil.SerialException as e:
    print(e)