from device.manless_device import Manless_device


class Manless:
    
    def __init__(self):
        self.manless = Manless_device('/dev/ttyACM2', 9600)        
        self.manless_status, self.message = self.manless.connect()
                                        
    def running(self):
        if self.manless.ser.isOpen():
            print("Connected To Manless Embedeed")                        
            while 1:
                data = self.manless.ser.readline()
                if len(data):
                    if data.strip() == 'MR':
                        print "Manless Ready"
                        self.manless.ser.write("SR")
                        self.manless.ser.flush()
                    if data.strip() == 'CD':
                        print "Car Detected"
                    if data.strip() == 'NCD': #No Car Detected
                        print "Car Not Detected"
                    if data.strip() == 'RT':
                        print "Request Ticket"
                        print "Waiting Ticket Process"
                        self.create_casual_trans()
                                                                    
                    if data.strip() == 'WP':
                        print "Waiting Process"
        else:
            print("Connect to Manless Embedeed Error")
            
            
    def create_casual_trans(self):
        print "Create Casual Trans"
        self.manless.ser.write("RTS\n")

    def create_member_trans(self):
        print "Create Member Trans"
    