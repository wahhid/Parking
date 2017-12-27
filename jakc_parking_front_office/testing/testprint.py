import serial

def line_feed(ser):
	data=[0x1b,0x64,0x01]	
	ser.write(data)

def print_barcode(ser,barcode):
	data=[0x1d,0x66,0x01]
	ser.write(data)
	data=[0x1d,0x48,0x32]
	ser.write(data)
	data=[0x1d,0x68,0x50]
	ser.write(data)
	data=[0x1d,0x77,0x02]
	ser.write(data)
	data=[0x1d,0x6b,0x43,0x0c]
	bar=data + barcode
	ser.write(bar)			
	
def toHex(s):
    lst = []
    for ch in s:
        hv=ord(ch)		
        lst.append('0x'+hv)
    
    return reduce(lambda x,y:x+y, lst)	
	
ser = serial.Serial()
ser.baudrate = 19200
ser.port = 7
ser.open()

print ser.name

ser.write(chr(27))
ser.write('@')

data=[0x1b,0x61,0x01]
ser.write(data)

data=[0x1b,0x45,0x01]
ser.write(data)

data=[0x1b,0x3d,0x01]
ser.write(data)
ser.write('Mal Taman Anggrek')
data=[0x1b,0x3d,0x02]
ser.write(data)

data=[0x1b,0x3d,0x01]
ser.write(data)
ser.write('Mal Taman Anggrek')
data=[0x1b,0x3d,0x02]
ser.write(data)

data=[0x1b,0x45,0x00]
ser.write(data)

line_feed(ser)
line_feed(ser)
line_feed(ser)
line_feed(ser)
line_feed(ser)
line_feed(ser)


#ser.write(chr(29)+chr(102)+chr(1))
#29#72#50
#ser.write(chr(29)+chr(72)+chr(50))
#29#104#80
#ser.write(chr(29)+chr(104)+chr(80))
data = [0x30, 0x31, 0x32, 0x30, 0x30, 0x30, 0x30, 0x34, 0x35, 0x36, 0x37, 0x38]
#data = toHex("120000456789")
# This is the string
#string = ''.join([chr(x) for x in data])
#ser.write(chr(29)+chr(107)+chr(67)+chr(12)+string)

print_barcode(ser,data)

line_feed(ser)
line_feed(ser)
line_feed(ser)

ser.write(chr(27))
ser.write('i')


ser.close()