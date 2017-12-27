from lib.park_openerp import park


class entry_manual_trans():
    
    def __init__(self):        
        self.park_openerp = park("localhost","8069","park_dev_7", "admin","P@ssw0rd")
        status, message = self.park_openerp.auth()
        if status:
            print "Auth Successfully"
        
    def create(self, values):               
        result, message = self.park_openerp.create_parking_transaction(values)
        if result:
            print "Create Transaction Successfully with ID : " + str(result)
        else:
            print "Error Create Transaction"
                   
    
    
entry = entry_manual_trans()
entry_booth_id = 1
entry_operator_id = 1
input_method = '1'
session_id, message = entry.park_openerp.request_session(entry_booth_id)
values = {}
values.update({'plat_number':'ba1477l'})
values.update({'session_id': session_id})
values.update({'input_method': input_method})
values.update({'entry_booth_id':entry_booth_id})
values.update({'entry_operator_id':entry_operator_id})
entry.create(values)
        
