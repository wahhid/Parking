import threading
import time

from device.manless_device import Manless_device


class EntryManless:
    
    def __init__(self):
        self.manless = Manless_device("/dev/ttyACM2", 9600)
        self.status, self.message = self.manless.connect()
        if not self.status:
            exit()
            
    def receive_data(self):
        if self.manless.ser.isOpen():
            print("Connected To Manless Embedeed")                        
            try:
                while 1:                
                    #data = self.manless.ser.readline()
                    #print data
                    #print "Send Data"
                    data = self.manless.ser.readline()
                    self.manless.ser.write("RTS\n")
                    time.sleep(0.5)
                     
            except Exception, e1:
                print "error communicating...: " + str(e1)                        
        else:
            print("Connect to Manless Embedeed Error")
            
    

entrymanless = EntryManless()

t1 = threading.Thread(target=entrymanless.receive_data())
t1.start()