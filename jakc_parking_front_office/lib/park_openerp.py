import base64
from xmlrpclib import Fault

from openerp.openerp import Openerp


class park(Openerp):
    
    def __init__(self, server, port, dbname, username, password):
        Openerp.__init__(self, server, port, dbname , username, password)        
        
    def request_session(self, booth_id):
        try:
            model = 'parking.transaction.session'
            values = {}
            values.update({'booth_id': booth_id})
            values.update({'operator_id': self.uid})        
            session_id = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction.session', 'create', values)
            return session_id, ""            
        except Fault as e:
            print e
            return False, e
        
    def get_session(self, session_id):
        try:
            args = [('id','=',session_id)]
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction.session', 'search', args)
            if ids:
                fields = []
                result =  self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction.session', 'read', [session_id],fields)
                return result[0], ""
            else:
                return False, "Transaction Session not Found"
        except Fault as e:
            return False, e        
    
    def create_parking_transaction(self, values):
        try:
            result = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction','create',values)
            return result, ""
        except Fault as e:
            return False, e
        
    def update_parking_transaction(self, trans_id, values):
        try:
            result = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction', 'write', [trans_id], values)
            return result, ""
        except Fault as e:
            return False, e

    def update_rfid_transaction(self, trans_id, values):
        try:
            result = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction', 'write', [trans_id], values)
            return result, ""
        except Fault as e:
            return False, e

            
    def get_parking_transaction(self, trans_id):
        try:
            args = [('id','=',trans_id)]
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction', 'search', args)
            if ids:
                fields = []
                result =  self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction', 'read', [trans_id],fields)
                return result[0], ""
            else:
                return False, "Transaction not Found"
        except Fault as e:
            return False, e

    def get_parking_transaction_charging(self, trans_id):
        try:
	    print trans_id
            args = [('trans_id','=',trans_id),('charging_type','=','casual')]
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction.charging', 'search', args)
            if ids:
		print ids
                fields = []
                result =  self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction.charging', 'read', ids,fields)
                return result[0], ""
            else:
                return False, "Transaction not Found"
        except Fault as e:
            return False, e
        
    def get_booth(self, booth_id):
        try:
            fields = []
            booths = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.booth', 'read', [booth_id], fields)
            if booths:                
                return booths[0] , ""
            else:
                return False, "Booth not Found"
        except Fault as e:
            return False, e
        
    def get_booth_by_booth_code(self, booth_code):        
        try:
            args = [('code','=', booth_code)]
            ids  = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.booth', 'search', args)
            if ids:                
                fields = []
                booths = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.booth', 'read', ids, fields)
                if booths:                    
                    return booths[0] , ""
            else:
                return False, "Booth not Found"
        except Fault as e:
            return False, e
        
    def get_booth_cameras(self, booth_id):
        try:
            args = [('booth_id','=', booth_id)]
            ids  = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.booth.camera', 'search', args)
            if ids:                
                fields = []
                booth_cameras = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.booth.camera', 'read', ids, fields)
                return booth_cameras , ""
            else:
                return False, "Booth Camera not Found"
        except Fault as e:
            return False, e
        

    def get_operator(self, operator_id):
        try:        
            fields = []
            operators = self.sock_object.execute(self.dbname, self.uid, self.password, 'hr.employee', 'read', [operator_id], fields)
            if operators:
                return operators[0], ""
            else:
                return False, "Operator not Found"
        except Fault as e:
            return False, e
    
    
    def get_operator_by_uid(self):
        try:
            args = [('user_id','=', self.uid)]
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'hr.employee', 'search', args)
            if ids:
                fields = []
                return self.sock_object.execute(self.dbname, self.uid, self.password, 'hr.employee', 'read', ids, fields)[0], ""
            else:
                return False, "Operator Information not Found"
        except Fault as e:
            return False, e

        
    def get_shift(self, shift_id):
        try:            
            fields = []
            shifts = self.sock_object(self.dbname, self.uid, self.password, 'parking.shift', 'read', [shift_id], fields)
            if shifts:
                return shifts[0], ""
            else:
                return False, "Shift not Found" 
        except Fault as e:
            return False, e

    def get_attachment(self, trans_id):
        try:
            fields = []
            attachments = self.sock_object.execute(self.dbname, self.uid, self.password, 'ir.attachment', 'read', [trans_id], fields)
            if attachments:
                return attachments[0], "" 
            else:
                return False, "Attachment not Found"
        except Fault as e:
            return False, e
    
    def get_active_drivers(self):
        try:
            args = [('is_valet_driver','=', True)]
            ids  = self.sock_object.execute(self.dbname, self.uid, self.password, 'hr.employee', 'search', args)
            if ids:                
                fields = ['otherid','name']
                drivers = self.sock_object.execute(self.dbname, self.uid, self.password, 'hr.employee', 'read', ids, fields)
                return drivers , ""
            else:
                return False, "Valet Driver not Found"
        except Fault as e:
            return False, e
                
    def get_driver(self, driver_nik):
        try:
            args = [('otherid','=',driver_nik)]
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'hr.employee', 'search', args)            
            fields = []
            employee = self.sock_object.execute(self.dbname, self.uid, self.password, 'hr.employee', 'read', ids, fields)
            if employee:
                return employee[0], ""
            else:
                return False, "Driver not Found"
        except Fault as e:
            return False, e
        
              
    def upload_image(self, name, trans_id, file_name, file_path, binary_field):        
        with open(file_path, "rb") as image_file:
            datas = base64.b64encode(image_file.read())
            
        values = {}
        values.update({'name':name})
        values.update({'res_id':trans_id})
        values.update({'res_model':'parking.transaction'})
        values.update({'trans_id': trans_id})
        values.update({'binary_field':binary_field})
        values.update({'datas_fname':file_name})
        values.update({'datas':datas})        
        return self.sock_object.execute(self.dbname, self.uid, self.password, 'ir.attachment', 'create', values)    

    def find_vehicle(self,carnumber):
        try:        
            args = [('plat_number','=',carnumber),('state','=','entry')]                            
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction', 'search', args)            
            fields = []
            trans =  self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction', 'read', ids, fields)
            if trans:                
                return trans[0],""                     
            else:
                return False, "Transaction not Found"
        except Fault as e:
            return False, e

    def rfid_find_vehicle(self,carnumber):
        try:
            args = [('plat_number','=',carnumber),'|',('state','=','entry'),('state','=','exit')]
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction', 'search', args)
            fields = []
            trans =  self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction', 'read', ids, fields)
            if trans:
                return trans[0],""
            else:
                return False, "Transaction not Found"
        except Fault as e:
            return False, e

    def get_pricing(self, pricing_id):
        try:                    
            fields = []
            pricing = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.pricing', 'read', [pricing_id], fields)
            if pricing:
                return pricing[0], ""
            else:
                return False, "Pricing not Found"
        except Fault as e:
            return False, e
       
    def get_pricing_by_code(self,pricing_code):
        try:                    
            args = [('code','=',pricing_code)]
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.pricing', 'search', args)            
            fields = []
            pricing = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.pricing', 'read', ids, fields)
            if pricing:
                return pricing[0], ""
            else:
                return False, "Pricing not Found"
        except Fault as e:
            return False, e

    def get_pricings_by_booth(self, booth_id):
        try:
            args = [('booth_id','=',booth_id)]
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.booth.pricing', 'search', args)
            fields = []
            result =  self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.booth.pricing', 'read', ids,fields)
            return result, ""
        except Fault as e:
            return False, e  
        
    def check_membership(self, card_number):
        try:
            args =[('card_number','=', card_number),('state','=','open')]
            ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.membership', 'search', args)
            if ids:                
                fields = []
                memberships = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.membership', 'read', ids, fields)
                if memberships:
                    args = [('plat_number','=', card_number),('state','=','entry')]
                    ids = self.sock_object.execute(self.dbname, self.uid, self.password, 'parking.transaction', 'search', args)
                    if ids:
                        return False, "Card In Use"
                    else:                        
                        return memberships[0], ""
                else:
                    return False, "Membership not Found" 
            else:
                return False, "Membership not Found"                    
        except Fault as e:
            return False, e                
