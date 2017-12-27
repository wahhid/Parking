import serial


class Manless_device:
    
    def __init__(self, port='/dev/ttyS0', speed=9600):                
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = speed
        self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        self.ser.timeout = 0             #non-block read
        #ser.timeout = 2              #timeout block read
        self.ser.xonxoff = False     #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2     #timeout for write        
                
    def connect(self):
        try: 
            self.ser.open()
            return True,""
        except Exception, e:
            print "error open serial port: " + str(e)
            return False,e 
    
    #def process(self):
    #    while True:
    #        data = self.ser.readline()
    #        if len(data) > 0:
    #            print data.strip()
    #            if data.strip() == 'RT':
    #                self.ser.write('RTS')
    #                print("Response Request Ticket")
    #            if data.strip() == 'CD':
    #                self.ser.write('RCK')
    #            print("Response Check Device")
    #        sleep(0.5)    