import logging
import pytz
from datetime import datetime
from pytz import timezone
from random import randint

from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('entry','Entry'),
    ('exit','Exit'),
    ('rfid','Rfid'),
    ('validated','Validated'),
    ('done','Close'),
    ('missing','Missing'),
    ('correction','Correction'),    
]

AVAILABLE_SESSION_STATES = [
    ('open','Open'),
    ('reopen','Re-Open'),
    ('done','Close'),
    ('post','Posted'),    
]

AVAILABLE_TRANS_TYPES = [
    ('0','Casual'),
    ('1','Member'),    
    ('2','Pinalty'),        
]


AVAILABLE_INPUT_METHODS = [
    ('0','Manless'),
    ('1','Operator'),    
    ('2','Manual'),                                
]

AVAILABLE_CHARGING_TYPES = [
    ('casual','Casual'),
    ('service','Service'),
    ('missing','Missing'),    
    ('pinalty','Pinalty'),
    ('voucher','Voucher'),            
    ('free', 'Free'),
]

class ir_attachment(osv.osv):
    _name = "ir.attachment"
    _inherit = "ir.attachment"
    _columns = {
        'binary_field' : fields.char('Binary Field', size=50),
        'trans_id': fields.many2one('parking.transaction','Transaction ID'),
    }
ir_attachment()

class parking_transaction_session(osv.osv):
    _name = "parking.transaction.session"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Parking Transaction Session"
    
    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    def trans_close(self, cr, uid, ids, values, context=None):
        values = {}
        values.update({'state': 'done'})
        return self.write(cr, uid, ids, values, context=context)
        
    def _close(self, cr, uid, ids, values, context=None):
        _logger.info("Start Close Parking Transaction Session")        
        args = [('session_id','=', ids[0]),('state','=', 'validated')]
        parking_transaction_ids = self.pool.get('parking.transaction').search(cr, uid, args, context=context)
        if parking_transaction_ids:
            _logger.info("Parking Transaction Found")
            datas = {}
            datas.update({'state':'done'})
            self.pool.get('parking.transaction').write(cr, uid, parking_transaction_ids, datas, context=context)
            self.message_post(cr, uid, ids[0], body="Transaction status change to <b>Close</b>", subtype='mt_comment', context=context)
        _logger.info("End Close Parking Transaction Session")
        return super(parking_transaction_session, self).write(cr, uid, ids, values, context=context)         
    
    def trans_re_open(self, cr, uid, ids, values, context=None):
        _logger.info("Start Transaction Re-Open")
        values = {}        
        values.update({'state': 'reopen'})        
        return self.write(cr, uid, ids, values, context=context)
                
    def _re_open(self, cr, uid, ids, values, context=None):                            
        values.update({'state': 'open'})
        self.message_post(cr, uid, ids[0], body="Transaction status change to <b>Open</b>", subtype='mt_comment', context=context)            
        return super(parking_transaction_session, self).write(cr, uid, ids, values, context=context)    

    def trans_request_correction(self, cr, uid, ids, context=None):
        _logger.info("Send Email")
        self.message_post(cr, uid, ids[0], body="Request For Correction to Admin", subtype='mt_comment', context=context)
                
    def trans_correction(self, cr, uid, ids, context=None):
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jakc_parking', 'view_parking_transaction_session_correction_form')
        view_id = view_ref and view_ref[1] or False
        context.update({'parking_transaction_session_id': ids[0]})
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Parking Transaction Session Correction',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'parking.transaction.session.correction',
            'context': context,            
            'target': 'new',
         } 
        
    def correction(self, cr, uid, ids, values, context=None):
        #self.message_post(cr, uid, ids[0], body="Correction", subtype='mt_comment', context=context)
        return super(parking_transaction_session, self).write(cr, uid, ids, values, context=context)
               
    def trans_receipt(self, cr, uid, ids, values, context=None):        
        _logger.info("Print Receipt for ID : " + str(ids))            
        id = ids[0]   
        config = self.pool.get('parking.config').get_config(cr, uid, context=context)
        serverUrl = 'http://' + config.report_server + ':' + config.report_server_port +'/jasperserver'
        j_username = config.report_user
        j_password = config.report_password
        ParentFolderUri = '/parking'
        reportUnit = '/parking/parking_session_receipt'
        url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&ID=' +  str(id) + '&decorate=no&j_username=' + j_username + '&j_password=' + j_password + '&output=pdf'
        return {
            'type':'ir.actions.act_url',
            'url': url,
            'nodestroy': True,
            'target': 'new' 
        }
                       
    def get_active_session(self, cr, uid, shift_id, booth_id, operator_id, context=None):
        args = [('shift_id','=' , shift_id),('booth_id','=',booth_id),('operator_id', '=' , operator_id),('session_date','=', datetime.now(timezone("Asia/Jakarta")).strftime('%Y-%m-%d'))]
        session_ids = self.search(cr, uid, args, context=context)
        if session_ids:
            return self.browse(cr, uid, session_ids[0], context=context)
        else:
            return False             
           
    def get_parking_transaction_count(self, cr, uid, ids, field_name, args, context=None):
        id = ids[0]
        res = {} 
        sql_req= "SELECT count(*) as total FROM parking_transaction a WHERE a.session_id=" + str(id) + " AND a.state='done'"        
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        
        if sql_res:
            total_trans = sql_res['total']
        else:
            total_trans = 0
                            
        res[id] = total_trans    
        return res         
                
    def get_parking_transaction_amount(self, cr, uid, ids, field_name, args, context=None):
        id = ids[0]
        res = {} 
        sql_req= "SELECT sum(total_amount) as total FROM parking_transaction a WHERE a.session_id=" + str(id) + " AND a.state='done'"        
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        
        if sql_res:
            total_trans = sql_res['total']
        else:
            total_trans = 0
                            
        res[id] = total_trans    
        return res         
        
    def get_parking_transaction_correction(self, cr, uid, ids, field_name, args, context=None):
        id = ids[0]
        res = {} 
        sql_req= "SELECT sum(total_amount) as total FROM parking_transaction a WHERE a.session_id=" + str(id) + " AND a.state='correction'"        
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        
        if sql_res:
            total_trans = sql_res['total']
        else:
            total_trans = 0
                            
        res[id] = total_trans    
        return res         
    
    def get_parking_transaction_pinalty(self, cr, uid, ids, field_name, args, context=None):
        id = ids[0]
        res = {} 
        sql_req= "SELECT sum(total_amount) as total FROM parking_transaction a WHERE a.session_id=" + str(id) + " AND trans_type='2' AND a.state='done'"        
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        
        if sql_res:
            total_trans = sql_res['total']
        else:
            total_trans = 0
                            
        res[id] = total_trans    
        return res         
        
    _columns = {
        'name': fields.char('Name', size=50, required=True, readonly=True),
        'session_date': fields.date('Session Date', required=True, readonly=True),
        'shift_id': fields.many2one('parking.shift', 'Shift', required=True, readonly=True),
        'booth_id': fields.many2one('parking.booth', 'Booth', required=True, readonly=True),
        'operator_id': fields.many2one('res.users','Operator', required=True, readonly=True),
        'total_trans': fields.function(get_parking_transaction_count, type="integer", string='Total Transaction'),
        'total_amount': fields.function(get_parking_transaction_amount, type="integer", string='Total Amount'),
        'total_pinalty': fields.function(get_parking_transaction_pinalty, type="integer", string='Total Pinalty'),
        'total_correction': fields.function(get_parking_transaction_correction, type="integer", string='Total Correction'),        
        'state' : fields.selection(AVAILABLE_SESSION_STATES, 'Status', size=16, readonly=True)                
    } 
    _defaults = {            
        'state': lambda *a : 'open',
    }
    
    def create(self, cr, uid, values, context=None):        
        shift = self.pool.get('parking.shift').get_current_shift(cr, uid, context=context)
        if not shift:
            raise osv.except_osv(('Error'), ('Shift not Found!'))
        booth = self.pool.get('parking.booth').get_trans(cr, uid, [values.get('booth_id')], context=context)                
        operator = self.pool.get('res.users').browse(cr, uid, values.get('operator_id'), context=context)            
        name = operator.name + " - " + booth.name + " -  " + shift.name         
        session = self.get_active_session(cr, uid, shift.id, values.get('booth_id'),values.get('operator_id'), context=context)
        if session:
            if session.state == 'done':
                values = {}
                self.trans_re_open(cr, uid, [session.id], values, context=context)                                    
            return session.id
        else:
            str_now = datetime.now(timezone("Asia/Jakarta"))
            session_date = str_now.strftime('%Y-%m-%d')
            values.update({'name': name})
            values.update({'shift_id': shift.id})
            values.update({'session_date': session_date})
            result = super(parking_transaction_session, self).create(cr, uid, values, context=context)
            return result
    
    def write(self, cr, uid, ids, values, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)
        
        if not trans:
            raise osv.except_osv(('Error'), ('Transaction not Found!'))
                
        if trans.state == 'done':            
            if 'state' in values.keys():
                _logger.info("State : " + values.get('state'))        
                if values.get('state') == 'reopen':                
                    return self._re_open(cr, uid, ids, values, context=context)
            else:
                raise osv.except_osv(('Warning'),   ('Transaction Reopen Failed!'))    
                    
            raise osv.except_osv(('Warning'),   ('Transaction Already Closed!'))                
        
        if 'state' in values.keys():                    
            if values.get('state') == 'done':
                return self._close(cr, uid, ids, values, context=context)
                    
        return super(parking_transaction_session, self).write(cr, uid, ids, values, context=context)
                
parking_transaction_session()

class parking_transaction(osv.osv):
    _name = "parking.transaction"

    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
        
    def _get_booth_code(self, cr, uid, booth_id, context=None):
        booth = self.pool.get('parking.booth').browse(cr, uid, booth_id, context=context)
        return booth.code
            
    
    def _generate_trans_id(self, cr, uid, context=None):        
        local_date = self._utc_to_local("Asia/Jakarta", datetime.now())
        prefix  = local_date.strftime('%Y%m%d%H%M%S%f')
        #number_seq = self.pool.get('ir.sequence').get(cr, uid, 'parking.transaction.sequence')[0] 
        return prefix
        
    def _check_vehicle(self, cr, uid, plat_number, context=None):        
        args = [('plat_number','=',plat_number),('state','=','entry')]        
        ids = self.search(cr, uid, args, context=context)
        if ids:
            return True
        else:
            return False
    
    def _is_member(self, cr, uid, ids, card_number, context=None):
        if ids:
            trans = self.get_trans(cr, uid, ids, context=context)
            args = [('card_number','=',card_number),('state','=','open')]
            ids = self.pool.get('parking.membership').search(cr, uid, args, context=context)
            if ids:                 
                membership_id = ids[0]
                payment_args = [('parking_membership_id','=',membership_id),('state','=','paid')]
                payment_ids = self.pool.get('parking.membership.payment').search(cr, uid, payment_args, order="start_date desc",context=context)
                if payment_ids:
                    payments = self.pool.get('parking.membership.payment').search(cr, uid, payment_args, context=context)
                    payment = payments[0]
                    if payment.end_date > trans.end_date and payment.start_date < trans.start_date:
                        return True
                    else:
                        return False                                                                                                                                                                            
            else:
                return False
        else:
            return False
        
    def _is_member_by_plat_number(self, cr, uid, ids, plat_number, context=None):
        if ids:
            trans = self.get_trans(cr, uid, ids, context=context)
            args = [('plat_number','=',plat_number),('state','=','open')]
            ids = self.pool.get('parking.membership').search(cr, uid, args, context=context)
            if ids:                 
                membership_id = ids[0]
                payment_args = [('parking_membership_id','=',membership_id),('state','=','paid')]
                payment_ids = self.pool.get('parking.membership.payment').search(cr, uid, payment_args, order="start_date desc",context=context)
                if payment_ids:
                    payments = self.pool.get('parking.membership.payment').search(cr, uid, payment_args, context=context)
                    payment = payments[0]
                    if payment.end_date > trans.end_date and payment.start_date < trans.start_date:
                        return True
                    else:
                        return False                                                                                                                                                                            
            else:
                return False
        else:
            return False
    
    def trans_close(self, cr, uid, ids, values, context=None):
        values = {}
        values.update({'state': 'done'})
        self.write(cr, uid, ids, values, context=context)
        
    def close(self, cr, uid, ids, values, context=None):            
        return super(parking_transaction, self).write(cr, uid, ids, values, context=context)
    
    def close_by_session(self, cr, uid, session_id, context=None):        
        sql_req = "UPDATE parking_transaction SET state='done' WHERE session_id=" + str(session_id) + " AND state='exit'"
        cr.execute(sql_req)
                
    def create_manless_transaction(self, cr, uid, values, context=None):
        _logger.info("Start Create Manless Transaction")
        #Find Shift
        shift = self.pool.get('parking.shift').get_current_shift(cr, uid, context=context)
        if not shift:    
            raise osv.except_osv(('Error'), ('Shift not Found!'))
                
        #Update Values Shift
        values.update({'entry_shift_id': shift.id})                
                
        #Generate Barcode
        barcode = self._random_with_N_digits(12)
                        
        if 'plat_number' in values.keys():
            #Using RFID Card            
            #values.update({'barcode':str(barcode)})
                                
            #Plat Number in Manless Values it's means using RFID Card                                        
            values.update({'card_number': values.get('plat_number')})
                            
            car_exist = self._check_vehicle(cr, uid, values.get('plat_number'), context=context)
            
            if car_exist:
                raise osv.except_osv(('Warning'), ('Member Already Used!'))

            is_member = self._is_member(cr, uid, values.get('plat_number'), context)            
                            
            if is_member:
                values.update({'trans_type':'1'}) #Trans type for Transaction Member                    
                values.update({'entry_member': True})
            else:
                #values.update({'trans_type':'1'})
                #values.update({'entry_member': False})
                raise osv.except_osv(('Warning'), ('You are not member'))            
        else:                
            #Push Button Transaction
            values.update({'barcode':str(barcode)})
            values.update({'plat_number':str(barcode)})
            values.update({'trans_type':'0'}) #Trans type for Transaction Casual
                                                            
        return super(parking_transaction, self).create(cr, uid, values, context=context)
        
    def create_operator_transaction(self, cr, uid, values, context=None):
        _logger.info("Start Create Operator Transaction")
        #Find Shift
        shift = self.pool.get('parking.shift').get_current_shift(cr, uid, context=context)
        if not shift:    
            raise osv.except_osv(('Error'), ('Shift not Found!'))
                
        #Update Values Shift
        values.update({'entry_shift_id': shift.id})                
        
        #Generate Barcode
        barcode = self._random_with_N_digits(12)        
        car_exist = self._check_vehicle(cr, uid, values.get('plat_number'), context=context)
        if car_exist:
            raise osv.except_osv(('Warning'), ('Car In Parking Area!'))
                            
        values.update({'barcode':str(barcode)})                                                        
        
        is_member = self._is_member_by_plat_number(cr, uid, None, values.get('plat_number'), context)
                
        if is_member:
            _logger.info('Car is member')
            values.update({'trans_type':'1'}) # Member Transaction                    
            values.update({'entry_member': True})
        else:
            values.update({'trans_type':'0'}) # Casual Transaction
            values.update({'entry_member': False})                                   
                                                
        return super(parking_transaction, self).create(cr, uid, values, context=context)
        
                
    def create_manual_transaction(self,cr, uid, values, context=None):
        _logger.info("Start Create Manual Transaction")
        
    def create_missing_transaction(self,cr, uid, values, context=None):
        _logger.info("Start Create Missing Transaction")
                
        #Find Shift
        shift = self.pool.get('parking.shift').get_current_shift(cr, uid, context=context)        
        if not shift:    
            raise osv.except_osv(('Error'), ('Shift not Found!'))
                
        #Update Values Shift
        values.update({'entry_shift_id': shift.id})                
        
        #Generate Barcode
        barcode = self._random_with_N_digits(12)                                    
        values.update({'barcode':str(barcode)})                                                        
        
        is_member = self._is_member_by_plat_number(cr, uid, None, values.get('plat_number'), context)
                
        if is_member:
            _logger.info('Car is member')
            values.update({'trans_type':'1'}) # Member Transaction                    
            values.update({'entry_member': True})
        else:
            values.update({'trans_type':'0'}) # Casual Transaction
            values.update({'entry_member': False})                                   
                                                
        return super(parking_transaction, self).create(cr, uid, values, context=context)        
        
                
    def _calculate_duration(self, cr, uid, ids, context=None):
        trans = self.get_trans(cr, uid, ids, context)
        
        years = 0
        month = 0
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        exit_datetime = datetime.strptime(trans.exit_datetime,'%Y-%m-%d %H:%M:%S')
        entry_datetime = datetime.strptime(trans.entry_datetime,'%Y-%m-%d %H:%M:%S')
        diff = exit_datetime - entry_datetime
        minutesandseconds = divmod(diff.days * 86400 + diff.seconds, 60)
        
        hours = minutesandseconds[0] / 60
        minutes = minutesandseconds[0] % 60
        seconds = minutesandseconds[1]        
          
        #diff = relativedelta(datetime.strptime(trans.exit_datetime,'%Y-%m-%d %H:%M:%S'),datetime.strptime(trans.entry_datetime,'%Y-%m-%d %H:%M:%S'))
        #years = diff.years
        #month = diff.months
        #hours = diff.hours
        #minutes = diff.minutes
        #seconds = diff.seconds
                
        values = {}
        values.update({'hours': hours})
        values.update({'minutes': minutes})
        values.update({'seconds': seconds})
        super(parking_transaction,self).write(cr, uid, ids, values, context=context)
        
    def _calculate_general_charge(self, cr, uid, ids, context=None):
        trans = self.get_trans(cr, uid, ids, context)
        pricing_id = trans.pricing_id
        if not pricing_id:
            raise osv.except_osv(('Warning'), ('Pricing not Available!'))
        
        if pricing_id.state != 'open':
            raise osv.except_osv(('Warning'), ('Pricing not allowed!'))
                 
        total_amount = 0        
        
        is_member = self._is_member(cr, uid, ids, trans.plat_number, context)
        
        if not is_member:
            if trans.hours == 0 and trans.minutes == 0 and trans.seconds > 0 : 
                total_amount = total_amount + pricing_id.first_hour_charge
    
            if trans.hours == 0 and trans.minutes > 0 : 
                total_amount = total_amount + pricing_id.first_hour_charge
            
            if trans.hours > 0:            
                #Calculate Hours
                if trans.hours == 1:
                    total_amount = total_amount + pricing_id.first_hour_charge
                if trans.hours == 2:
                    total_amount = total_amount + pricing_id.first_hour_charge
                    total_amount = total_amount + pricing_id.second_hour_charge
                if trans.hours >= 3 :
                    total_amount = total_amount + pricing_id.first_hour_charge
                    total_amount = total_amount + pricing_id.second_hour_charge                
                    total_amount = total_amount + pricing_id.third_hour_charge
                    next_hours = trans.hours - 3                            
                    total_amount = total_amount + (next_hours * pricing_id.next_hour_charge)             
                #Calculate Minutes
                if trans.minutes > 0:            
                    total_amount = total_amount + pricing_id.next_hour_charge
                                                    
        values = {}
        values.update({'trans_id': trans.id})
        values.update({'charging_type': 'casual'})
        values.update({'total_charging': total_amount})
        result = self.pool.get('parking.transaction.charging').create(cr, uid, values, context=context)
               
    def _calculate_service_charge(self, cr, uid, ids, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)
        pricing_id = trans.pricing_id
        
        if pricing_id.service_charge > 0:
            if pricing_id.state != 'open':
                raise osv.except_osv(('Warning'), ('Pricing not allowed!'))              
            
            total_amount = 0
            
            is_member = self._is_member(cr, uid, ids, trans.plat_number, context);
            
            if not is_member:
                if trans.hours > 0 or trans.minutes > 0 or trans.seconds > 0 :                                
                    total_amount = total_amount + pricing_id.service_charge
                    
            values = {}
            values.update({'trans_id': trans.id})
            values.update({'charging_type': 'service'})
            values.update({'total_charging': total_amount})
            result = self.pool.get('parking.transaction.charging').create(cr, uid, values, context=context)
    
    def _calculate_missing_charge(self, cr, uid, ids, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)
        pricing_id = trans.pricing_id
        
        if pricing_id.state != 'open':
            raise osv.except_osv(('Warning'), ('Pricing not allowed!'))              
        
        total_amount = 0
                    
        values = {}
        values.update({'trans_id': trans.id})
        values.update({'charging_type': 'missing'})
        values.update({'total_charging': pricing_id.pinalty_charge})
        result = self.pool.get('parking.transaction.charging').create(cr, uid, values, context=context)
        
    def _calculate_total_amount(self, cr, uid, ids, context=None):
        trans = self.get_trans(cr, uid, ids, context)
        total_amount = 0
        for charging in trans.charging_ids:        
            #total_amount = trans.casual_charging + trans.service_charging + trans.pinalty_charging - trans.voucher_charging
            total_amount = total_amount + charging.total_charging
        
        values = {}
        values.update({'total_amount': total_amount})    
        super(parking_transaction,self).write(cr, uid, ids, values, context=context)
        
    def _get_binary_filesystem(self, cr, uid, ids, name, arg, context=None):
        """ Display the binary from ir.attachment, if already exist """
        res = {}
        attachment_obj = self.pool.get('ir.attachment')
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = False
            #attachment_ids = attachment_obj.search(cr, uid, [('res_model','=',self._name),('res_id','=',record.id),('binary_field','=',name)], context=context)
            attachment_ids = attachment_obj.search(cr, uid, [('res_model','=',self._name),('res_id','=',record.id),('binary_field','=',name)], context=context)
            import logging
            _logger = logging.getLogger(__name__)
            _logger.info('res %s', attachment_ids)
            if attachment_ids:
                img  = attachment_obj.browse(cr, uid, attachment_ids, context=context)[0].datas                
                res[record.id] = img
        return res
    
    def _set_binary_filesystem(self, cr, uid, id, name, value, arg, context=None):
        """ Create or update the binary in ir.attachment when we save the record """
        attachment_obj = self.pool.get('ir.attachment')
        #attachment_ids = attachment_obj.search(cr, uid, [('res_model','=',self._name),('res_id','=',id),('binary_field','=',name)], context=context)
        attachment_ids = attachment_obj.search(cr, uid, [('res_model','=',self._name),('res_id','=',id),('binary_field','=',name)], context=context)        
        if value:
            if attachment_ids:
                attachment_obj.write(cr, uid, attachment_ids, {'datas': value}, context=context)
            else:
                attachment_obj.create(cr, uid, {'res_model': self._name, 'res_id': id, 'name': 'Marketplace picture', 'binary_field': name, 'datas': value, 'datas_fname':'picture.jpg'}, context=context)
        else:
            attachment_obj.unlink(cr, uid, attachment_ids, context=context)
            
    def _random_with_N_digits(self, number_digit):
        range_start = 10**(number_digit-1)
        range_end = (10**number_digit)-1
        return randint(range_start, range_end)
            
    def _close_session_transaction(self, cr, uid, session_id, context=None):        
        sql_req = "UPDATE parking_transaction SET state='done' WHERE session_id=" + str(session_id) + " AND state='exit'"
        result = cr.execute(sql_req)
            
    def _utc_to_local(self, timezone, current_date):        
        tzinfo_local = pytz.timezone(timezone)        
        tzinfo_utc = pytz.timezone("UTC")        
        utc_date = tzinfo_utc.localize(current_date, is_dst=None)
        local_date = utc_date.astimezone(tzinfo_local)
        return local_date
    
    def _local_to_utc(self, timezone, str_datetime):
        tzinfo = pytz.timezone(timezone)
        utc_datetime = datetime.strptime(str_datetime,'%Y-%m-%d %H:%M:%S')
        local_datetime = tzinfo.localize(utc_datetime, is_dst=None)
        utc = local_datetime.astimezone(pytz.utc)
        return utc

        
            
    _columns = {
        'session_id': fields.many2one('parking.transaction.session','Session',readonly=True),
        'trans_id': fields.char('Transaction #', size=21, required=True, readonly=True),
        'barcode': fields.char('Barcode #', size=13, required=True, readonly=True),
        'card': fields.char('Card #', size=20),
        'trans_type': fields.selection(AVAILABLE_TRANS_TYPES, 'Transaction Type', size=16, required=True, readonly=True),
        'plat_number': fields.char('Plat Number', size=21, required=True),
        'card_number': fields.char('Card Number', size=20, readonly=True),
        'sequence_number':fields.char('Sequence #', size=10, readonly=True),
        'input_method': fields.selection(AVAILABLE_INPUT_METHODS, 'Method'),
        'is_manual': fields.boolean('Is Manual', readonly=True),
        'is_pinalty': fields.boolean('Is Pinalty', readonly=True),
        'entry_datetime': fields.datetime('Entry Date Time', required=True),
        'entry_member': fields.boolean('Entry Member'),
        'entry_booth_id': fields.many2one('parking.booth','Entry Booth', required=True),
        'entry_operator_id': fields.many2one('hr.employee','Entry Operator', required=True),
        'entry_driver_id': fields.many2one('hr.employee','Entry Driver'),
        'entry_shift_id': fields.many2one('parking.shift', 'Entry Shift', required=True),
        'exit_datetime': fields.datetime('Exit Date Time'),
        'exit_member': fields.boolean('Exit Member'),
        'exit_booth_id': fields.many2one('parking.booth','Exit Booth'),
        'exit_operator_id': fields.many2one('hr.employee','Exit Operator'),
        'exit_driver_id': fields.many2one('hr.employee','Exit Driver'),
        'exit_shift_id': fields.many2one('parking.shift', 'Exit Shift'),
        'hours': fields.float('Hours', readonly=True),
        'minutes': fields.float('Minutes', readonly=True),
        'seconds': fields.float('Seconds', readonly=True),        
        'pricing_id': fields.many2one('parking.pricing', 'Pricing'),
        'casual_charging': fields.float('Casual Charging' , readonly=True),
        'service_charging': fields.float('Service Charging' , readonly=True),        
        'pinalty_charging': fields.float('Pinalty Charging' , readonly=True),
        'voucher_charging': fields.float('Voucher Charging', readonly=True),
        'rules_charging': fields.float('Rules Charging', readonly=True),        
        'total_amount': fields.float('Total Charging', readonly=True),
        'entry_front_image': fields.function(_get_binary_filesystem, fnct_inv=_set_binary_filesystem, type='binary', string='Entry Front'),
        'exit_front_image': fields.function(_get_binary_filesystem, fnct_inv=_set_binary_filesystem, type='binary', string='Exit Front'),        
        'attach_ids':fields.one2many('ir.attachment', 'trans_id', 'Image Attachment',  ondelete='cascade'),
        'image_ids': fields.many2many('ir.attachment', 'parking_transaction_attachment_rel', 'trans_id', 'image_id', 'Images',  ondelete='cascade'),
        'charging_ids': fields.one2many('parking.transaction.charging','trans_id','Chargings',  ondelete='cascade'),
        'correction_ids': fields.one2many('parking.transaction.correction','trans_id','Corrections',  ondelete='cascade'),
        'state': fields.selection(AVAILABLE_STATES,'Status', size=16, readonly=True),
    }
    
    _defaults = {
        'entry_datetime': lambda *a: fields.datetime.now(),
        'is_manual': lambda *a: False,
        'is_pinalty': lambda *a: False,
        'entry_member': lambda *a: False,
        'exit_member': lambda *a: False,
        'casual_charging': lambda *a: 0,
        'service_charging': lambda *a: 0,
        'pinalty_charging': lambda *a: 0,
        'voucher_charging': lambda *a: 0,
        'rules_charging': lambda *a: 0,
        'total_amount': lambda *a: 0,
        'state': lambda *a: 'entry',
    }
    
       
    def create(self, cr, uid, values, context=None):        
        #Generate Transaction ID
        trans_id = self._generate_trans_id(cr, uid, context=context)
                
        booth_id = values.get('entry_booth_id')        
        if not booth_id:
            raise osv.except_osv(('Warning'),   ('Booth not defined!'))
          
        booth = self.pool.get('parking.booth').get_trans(cr, uid, [booth_id], context=context)                                                  
        trans_id = booth['code'] + trans_id
        if booth.with_sequence:
            sequence_number = self.pool.get('parking.booth').generate_sequence_number(cr, uid, [booth.id], context=context)
            values.update({'sequence_number': sequence_number})
            
        if 'state' in values.keys():
            
            if values.get('state') == 'missing':                   
                
                values.update({'trans_id':trans_id})
                values.update({'input_method': '1'})
                values.update({'state': 'entry'})
                utc_entry_datetime = self._local_to_utc("Asia/Jakarta", values.get('entry_datetime'))
                #tzinfo = pytz.timezone("Asia/Jakarta")
                #entry_datetime = datetime.strptime(values.get('entry_datetime'),'%Y-%m-%d %H:%M:%S')
                #local_entry_datetime = tzinfo.localize(entry_datetime, is_dst=None)
                #utc_entry_datetime = local_entry_datetime.astimezone(pytz.utc)
                    
                values.update({'entry_datetime': utc_entry_datetime.strftime('%Y-%m-%d %H:%M:%S')})
                
                result = self.create_missing_transaction(cr, uid, values, context=context)                
                ids = [result]                                                  
                
                trans = self.get_trans(cr, uid, ids, context=context)
                
                if trans.state != 'entry':
                    raise osv.except_osv(('Warning'), ('Please Complete Entry Transaction!'))
                
                #Update Exit Shift
                shift = self.pool.get('parking.shift').get_current_shift(cr, uid, context=context)        
                if not shift:            
                    raise osv.except_osv(('Error'), ('Shift not Found!'))
                        
                values.update({'exit_shift_id': shift.id})
                
                #Transaction Type Pinalty            
                values.update({'trans_type': '2'})
                exit_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                values.update({'exit_datetime':exit_datetime})
                values.update({'exit_booth_id': values.get('entry_booth_id')})                
                values.update({'exit_operator_id': values.get('entry_operator_id')})
                values.update({'state': 'exit'})
                                
                super(parking_transaction,self).write(cr, uid, ids, values, context=context)
                
                #Calculate Duration
                self._calculate_duration(cr, uid, ids, context=context)
                                            
                #Calculate General Charge
                self._calculate_general_charge(cr, uid, ids, context=context)              
                
                #Calculate Service Charge
                self._calculate_service_charge(cr, uid, ids, context=context)                                            
                    
                #Calcuate Missing Ticket Charge
                self._calculate_missing_charge(cr, uid, ids, context=context)
                
                #Calculate Total Amount
                self._calculate_total_amount(cr, uid, ids, context=context)
                            
                return trans.id              
        else:                  
            if values.get('input_method') == '0': # Manless
                values.update({'trans_id':trans_id})
                return self.create_manless_transaction(cr, uid, values, context=context)
            
            elif values.get('input_method') == '1': # Operator
                values.update({'trans_id':trans_id})
                return self.create_operator_transaction(cr, uid, values, context=context)        
    
            elif values.get('input_method') == '2': # Manual
                values.update({'trans_id':trans_id})            
                return self.create_manual_transaction(cr, uid, values, context=context)
            
            else:
                raise osv.except_osv(('Warning'),   ('Method not defined!'))  
                        
    
    def write(self, cr, uid, ids, values, context=None):              
        
        trans  = self.get_trans(cr, uid, ids, context=context)     

        if not trans:
            raise osv.except_osv(('Error'), ('Transaction not Found!'))
                
        if trans.state == 'done':
            raise osv.except_osv(('Warning'),   ('Transaction Already Closed!'))                
                    
        if 'state' in values.keys():

            if values.get('state') == 'rfid':
                if trans.state == 'entry':
                    values.update({'state':'entry'})
                    return super(parking_transaction, self).write(cr, uid, ids, values, context=context)
                elif trans.state == 'exit':
                    values.update({'state':'validated'})
                    return super(parking_transaction, self).write(cr, uid, ids, values, context=context)
                else:
                    return True

            if values.get('state') == 'exit':
                
                if trans.state != 'entry':
                    raise osv.except_osv(('Warning'), ('Please Complete Entry Transaction!'))
                
                #Update Exit Shift
                shift = self.pool.get('parking.shift').get_current_shift(cr, uid, context=context)        
                if not shift:            
                    raise osv.except_osv(('Error'), ('Shift not Found!'))
                        
                values.update({'exit_shift_id': shift.id})            
                
                exit_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                values.update({'exit_datetime':exit_datetime})
                #values.update({'state': 'done'})
                super(parking_transaction,self).write(cr, uid, ids, values, context=context)
                
                #Calculate Duration
                self._calculate_duration(cr, uid, ids, context=context)
                                
                #Check Membership
                #is_member = self._is_member(cr, uid, trans.plat_number, context)                                                
                
                #Calculate General Charge
                self._calculate_general_charge(cr, uid, ids, context=context)              
                
                #Calculate Service Charge
                self._calculate_service_charge(cr, uid, ids, context=context)                                            
                    
                #Calculate Total Amount
                self._calculate_total_amount(cr, uid, ids, context=context)
                            
                return True
            
            if  values.get('state') == 'missing':
                
                if trans.state != 'entry':
                    raise osv.except_osv(('Warning'), ('Please Complete Entry Transaction!'))
                
                #Update Exit Shift
                shift = self.pool.get('parking.shift').get_current_shift(cr, uid, context=context)        
                if not shift:            
                    raise osv.except_osv(('Error'), ('Shift not Found!'))
                        
                values.update({'exit_shift_id': shift.id})
                
                #Transaction Type Pinalty            
                values.update({'trans_type': '2'})
                
                exit_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')                
                values.update({'exit_datetime':exit_datetime})
                values.update({'state': 'exit'})
                super(parking_transaction,self).write(cr, uid, ids, values, context=context)
                
                #Calculate Duration
                self._calculate_duration(cr, uid, ids, context=context)
                                
                #Check Membership
                #is_member = self._is_member(cr, uid, trans.plat_number, context)                                                
                
                #Calculate General Charge
                self._calculate_general_charge(cr, uid, ids, context=context)              
                
                #Calculate Service Charge
                self._calculate_service_charge(cr, uid, ids, context=context)                                            
                    
                #Calcuate Missing Ticket Charge
                self._calculate_missing_charge(cr, uid, ids, context=context)
                
                #Calculate Total Amount
                self._calculate_total_amount(cr, uid, ids, context=context)
                            
                return True
            
        return super(parking_transaction,self).write(cr, uid, ids, values, context=context)             

parking_transaction() 


class parking_transaction_charging(osv.osv):
    _name = "parking.transaction.charging"
    _decription = "Parking Transaction Charging"
    
    _columns = {
        'trans_id': fields.many2one('parking.transaction', 'Transaction ID', readonly=True),
        'charging_type' : fields.selection(AVAILABLE_CHARGING_TYPES,'Charging Type', required=True, readonly=True),
        'total_charging': fields.float('Total Charging'),
    }
        
parking_transaction_charging()    

class parking_transaction_correction(osv.osv):
    _name = "parking.transaction.correction"
    _description = "Parking Transaction Correction"
    _columns = {
        'trans_id': fields.many2one('parking.transaction', 'Transaction ID', readonly=True),
        'new_trans_id': fields.many2one('parking.transaction', 'Transaction ID', readonly=True),
        'remarks': fields.text('Remarks'),        
    }
    
parking_transaction_correction()
