from lib.park_openerp import park


class exit_manual_trans():
    
    def __init__(self):        
        self.park_openerp = park("localhost","8069","park_dev_7", "admin","P@ssw0rd")
        status, message = self.park_openerp.auth()
        if status:
            print "Auth Successfully"
        
    def write(self, trans_id, values):               
        result, message = self.park_openerp.update_parking_transaction(trans_id, values)
        if result:
            print  "Transaction Successfully with ID : " + str(result)
        else:
            print "Error Create Transaction"
             
      
exit = exit_manual_trans()
trans, message = exit.park_openerp.find_vehicle("ba1488l")
if trans:
    exit_booth_id = 4
    exit_operator_id = 1
    pricing_id = 1
    session_id, message = exit.park_openerp.request_session(exit_booth_id)
    values = {}
    values.update({'session_id': session_id})
    values.update({'exit_booth_id': exit_booth_id})        
    values.update({'exit_operator_id': exit_operator_id})
    values.update({'pricing_id': pricing_id})            
    values.update({'state':'exit'})
    result, message = exit.write(trans['id'], values)
else:
    print "Error Exit Process"