import serial

line = []

try:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=0.5)
    print("Connected Bill Acceptor")
    while True:

        #print "--------------------------------"
        #thestring = "\x02\x08\x10\x7F\x10\x7F\x03\x08"
        thestring = "\x02\x08\x10\x1F\x10\x00\x03\x17"        
        ser.write(thestring)        
        print "Sent : Pooling  - [" + thestring + "]"
        data = ser.read(11)
        if data:
            print "Receive : Pooling  [" + data + "]"
            thestring = "\x02\x08\x11\x7F\x10\x7F\x03\x09"        
            ser.write(thestring)
            data = ser.read(11)                            
        else:
            print "No Data"
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
    
except serial.SerialTimeoutException:
            print "Serial read timeout"  
except serial.serialutil.SerialException as e:
    print(e)