import threading

from openerp import openerp

from manless import Manless


class manless_thread(Manless):
    
    def __init__(self):
        Manless.__init__(self)
        self.openerp = openerp.Openerp(self, 'localhost', '8069', 'park_dev_7', 'admin', 'P@ssw0rd')
        result = self.openerp.auth()        
        if not result:
            exit()
    
    def create_casual_trans(self):
        print "Create Casual Trans - Thread"
        values = {}
        values.update({'is_manless': True})        
        values.update({'entry_booth_id':1})
        values.update({'entry_shift_id':1})
        values.update({'entry_operator_id':1})   
        result, message = self.openerp.create_parking_transaction(values)
        
        

entrymanless = manless_thread()
t1 = threading.Thread(target=entrymanless.running())
t1.daemon = True