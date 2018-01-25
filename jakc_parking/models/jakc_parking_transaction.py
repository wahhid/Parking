import logging
import pytz
from datetime import datetime
from pytz import timezone
from random import randint

from openerp import models, fields, api
from openerp.exceptions import ValidationError, Warning

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('draft','Draft'),
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


class ParkingTransactionSession(models.Model):
    _name = "parking.transaction.session"
    _inherit = ['mail.thread']
    _description = "Parking Transaction Session"

    @api.one
    def trans_close(self):
        session = self
        parking_transaction_ids = session.parking_transaction_ids
        parking_transaction_ids.write({'state':'done'})
        values = {}
        values.update({'state': 'done'})
        self.write(values)
        
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
        return super(ParkingTransactionSession, self).write(values)

    @api.one
    def trans_re_open(self):
        values = {}        
        values.update({'state': 'reopen'})        
        super(ParkingTransactionSession,self).write(values)
        self.message_post("Transaction status change to <Open</b>")

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
        
    def correction(self, values):
        #self.message_post(cr, uid, ids[0], body="Correction", subtype='mt_comment', context=context)
        return super(ParkingTransactionSession, self).write(values)
               
    def trans_receipt(self):
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
                       
    def get_active_session(self, shift_id, booth_id, operator_id):
        args = [('shift_id','=' , shift_id),('booth_id','=',booth_id),('operator_id', '=' , operator_id),('session_date','=', datetime.now(timezone("Asia/Jakarta")).strftime('%Y-%m-%d'))]
        session_ids = self.search(args)
        if len(session_ids) > 0:
            return session_ids[0]
        else:
            return False             

    @api.one
    def get_parking_transaction_count(self):
        sql_req= "SELECT count(*) as total FROM parking_transaction a WHERE a.session_id=" + str(self.id) + " AND a.state='done'"
        self.env.cr.execute(sql_req)
        sql_res = self.env.cr.dictfetchone()

        if sql_res:
            self.total_trans = sql_res['total']
        else:
            self.total_trans = 0

    @api.one
    def get_parking_transaction_amount(self):
        sql_req= "SELECT sum(total_amount) as total FROM parking_transaction a WHERE a.session_id=" + str(self.id) + " AND a.state='done'"
        self.env.cr.execute(sql_req)
        sql_res = self.env.cr.dictfetchone()
        
        if sql_res:
            self.total_amount = sql_res['total']
        else:
            self.total_amount = 0

    @api.one
    def get_parking_transaction_correction(self):
        sql_req= "SELECT sum(total_amount) as total FROM parking_transaction a WHERE a.session_id=" + str(self.id) + " AND a.state='correction'"
        self.env.cr.execute(sql_req)
        sql_res = self.env.cr.dictfetchone()
        if sql_res:
            self.total_correction = sql_res['total']
        else:
            self.total_correction = 0

    @api.one
    def get_parking_transaction_pinalty(self):
        sql_req= "SELECT sum(total_amount) as total FROM parking_transaction a WHERE a.session_id=" + str(self.id) + " AND a.state='done'"
        self.env.cr.execute(sql_req)
        sql_res = self.env.cr.dictfetchone()
        
        if sql_res:
            self.total_pinalty = sql_res['total']
        else:
            self.total_pinalty = 0

    name = fields.Char('Name', size=50, required=True, readonly=True)
    session_date = fields.Date('Session Date', required=True, readonly=True)
    shift_id = fields.Many2one('parking.shift', 'Shift', required=True, readonly=True)
    booth_id = fields.Many2one('parking.booth', 'Booth', required=True, readonly=True)
    operator_id = fields.Many2one('res.users', 'Operator', required=True, readonly=True)
    total_trans = fields.Float(compute='get_parking_transaction_count', string='Total Transaction')
    total_amount = fields.Float(compute='get_parking_transaction_amount', string='Total Amount')
    total_pinalty = fields.Float(compute='get_parking_transaction_pinalty', string='Total Pinalty')
    total_correction = fields.Float(compute='get_parking_transaction_correction', string='Total Correction')
    parking_transaction_ids = fields.One2many('parking.transaction','session_id','Transaction')
    state = fields.Selection(AVAILABLE_SESSION_STATES, 'Status', size=16, readonly=True, default='open')

    @api.model
    def create(self, values):
        parking_shift_obj = self.env['parking.shift']
        parking_booth_obj = self.env['parking.booth']
        res_users_obj = self.env['res.users']

        shift = parking_shift_obj.get_current_shift()
        if not shift:
            raise ValidationError('Shift not Found')

        session = self.get_active_session(shift.id, values.get('booth_id'),values.get('operator_id'))
        if session:
            return session.id
        else:
            if 'booth_id' not in values.keys():
                raise ValidationError('Booth not Found')
            booth = parking_booth_obj.browse(values.get('booth_id'))

            if 'operator_id' not in values.keys():
                raise ValidationError('Booth not Found')
            operator = res_users_obj.browse(values.get('operator_id'))

            name = operator.name + " - " + booth.name + " -  " + shift.name
            str_now = datetime.now(timezone("Asia/Jakarta"))
            session_date = str_now.strftime('%Y-%m-%d')
            values.update({'name': name})
            values.update({'shift_id': shift.id})
            values.update({'session_date': session_date})
            result = super(ParkingTransactionSession, self).create(values)
            return result

    def write(self, values):
        session = self
        if session.state == 'done':
            raise ValidationError('Transaction Already Closed!')

        return super(ParkingTransactionSession, self).write(values)


class ParkingTransaction(models.Model):
    _name = "parking.transaction"

    def _get_booth_code(self, booth_id):
        booth = self.env['parking.booth'].browse(booth_id)
        if booth:
            return booth.code
        else:
            return False
    
    def _generate_trans_id(self):
        local_date = self._utc_to_local("Asia/Jakarta", datetime.now())
        prefix  = local_date.strftime('%Y%m%d%H%M%S%f')
        return prefix
        
    def _check_vehicle(self, plat_number):
        args = [('plat_number','=',plat_number),('state','=','entry')]        
        parking_transaction_ids = self.search(args)
        if len(parking_transaction_ids) > 0:
            return parking_transaction_ids[0]
        else:
            return False
    
    def _is_member_by_card_number(self, card_number):
        parking_transaction = self
        args = [('card_number','=',card_number),('state','=','open')]
        parking_membership_ids = self.env['parking.membership'].search(args)
        if len(parking_membership_ids) > 0:
            parking_membership = parking_membership_ids[0]
            payment_args = [('parking_membership_id', '=', parking_membership.id), ('state', '=', 'paid')]
            parking_membership_payment_ids = self.env['parking.membership.payment'].search(payment_args)
            if len(parking_membership_payment_ids)>0:
                parking_membership_payment = parking_membership_payment_ids[0]
                if parking_membership_payment.end_date > parking_transaction.end_date and parking_membership_payment.start_date < parking_transaction.start_date:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
    def _is_member_by_plat_number(self, plat_number):
        parking_transaction = self
        args = [('plat_number','=',plat_number),('state','=','open')]
        parking_membership_ids = self.env['parking.membership'].search(args)
        if len(parking_membership_ids)>0:
            parking_membership = parking_membership_ids[0]
            payment_args = [('parking_membership_id','=',parking_membership.id),('state','=','paid')]
            parking_membership_payment_ids = self.env['parking.membership.payment'].search(payment_args, order="start_date desc")
            if len(parking_membership_payment_ids)>0:
                parking_membership_payment = parking_membership_payment_ids[0]
                if parking_membership_payment.end_date > parking_transaction.end_date and parking_membership_payment.start_date < parking_transaction.start_date:
                    return True
                else:
                    return False
        else:
            return False

    def prepare_entry_manless_transaction(self, values):
        _logger.info("Start Create Manless Transaction")
        parking_booth_obj = self.env['parking.booth']
        parking_shift_obj = self.env['parking.shift']

        booth = parking_booth_obj.browse(values.get('booth_id'))
        if not booth:
            raise ValidationError('Booth not Found!')

        shift = parking_shift_obj.get_current_shift()
        if not shift:
            raise ValidationError('Shift not Found!')

        values.update({'entry_shift_id': shift.id})

        if booth.booth_type == '0':
            # Entry Booth
            values.update({'entry_booth_id': booth.id})

            # Fill Entry Date Time
            utc_date = self._local_to_utc("Asia/Jakarta", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            values.update({'entry_datetime': utc_date})

            # Generate Barcode
            barcode = self._random_with_N_digits(12)

            if 'plat_number' in values.keys():
                # Using RFID Card
                trans = self._check_vehicle(values.get('plat_number'))
                if trans:
                    raise ValidationError('Member Already Used!')

                values.update({'card_number': values.get('plat_number')})
                is_member = self._is_member_by_card_number(values.get('plat_number'))
                if is_member:
                    values.update({'trans_type': '1'})  # Trans type for Transaction Member
                    values.update({'entry_member': True})
                else:
                    raise ValidationError('Invalid Card')
            else:
                # Push Button Transaction
                values.update({'barcode': str(barcode)})
                values.update({'plat_number': str(barcode)})
                values.update({'trans_type': '0'})  # Trans type for Transaction Casual

            return super(ParkingTransaction,self).create(values)
        else:
            raise ValidationError('Booth not valid!')

    def prepare_entry_operator_transaction(self, values):
        _logger.info("Start Create Operator Transaction")
        parking_booth_obj = self.env['parking.booth']
        parking_shift_obj = self.env['parking.shift']

        booth = parking_booth_obj.browse(values.get('booth_id'))
        if not booth:
            raise ValidationError('Booth not Found!')

        #Get Current Shift
        shift = parking_shift_obj.get_current_shift()
        if not shift:
            raise ValidationError('Shift not Found!')
        values.update({'entry_shift_id': shift.id})

        if booth.booth_type == '0':
            # Check Car In Area
            trans  = self._check_vehicle(values.get('plat_number'))
            if trans:
                raise ValidationError('Car In Parking Area!')

            #Entry Booth
            values.update({'entry_booth_id': booth.id})

            #Generate Trans ID
            values.update({'trans_id': self._generate_trans_id()})

            #Fill Entry Date Time
            utc_date = self._local_to_utc("Asia/Jakarta", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            values.update({'entry_datetime': datetime.now()})

            # Generate Barcode
            barcode = self._random_with_N_digits(12)
            values.update({'barcode': str(barcode)})

            #Check Member Status
            is_member = self._is_member_by_plat_number(values.get('plat_number'))

            if is_member:
                _logger.info('Car is member')
                values.update({'trans_type': '1'})  # Member Transaction
                values.update({'entry_member': True})
            else:
                values.update({'trans_type': '0'})  # Casual Transaction
                values.update({'entry_member': False})

            #Set State to Entry
            values.update({'state':'entry'})

            return super(ParkingTransaction, self).create(values)
        elif booth.booth_type == '1':
            # Entry Booth
            values.update({'exit_booth_id': booth.id})

            #Exit Transaction
            trans = self._check_vehicle(values.get('plat_number'))
            if not trans:
                raise ValidationError('Car not exist!')

            # Fill Entry Date Time
            utc_date = self._local_to_utc("Asia/Jakarta", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            values.update({'exit_datetime': utc_date})

            # Check Member Status
            is_member = self._is_member_by_plat_number(values.get('plat_number'))

            if is_member:
                _logger.info('Car is member')
                values.update({'trans_type': '1'})  # Member Transaction
                values.update({'exit_member': True})
            else:
                values.update({'trans_type': '0'})  # Casual Transaction
                values.update({'exit_member': False})

            # Set State to Exit
            values.update({'state': 'exit'})

            trans.write(values)
            trans.calculate_duration()
            trans.calculate_general_charge()
            trans.calculate_service_charge()
            trans.calculate_total_amount()

            return trans

        else:
            #Entry or Exit Transaction
            car_exist = self._check_vehicle(values.get('plat_number'))

    def prepare_entry_manual_transaction(self, values):
        _logger.info("Start Create Manual Transaction")
        return super(ParkingTransaction, self).create(values)

    def prepare_entry_missing_transaction(self, values):
        _logger.info("Start Create Missing Transaction")

        # Find Shift
        shift = self.pool.get('parking.shift').get_current_shift()
        if not shift:
            raise ValidationError('Shift not Found!')

        # Update Values Shift
        values.update({'entry_shift_id': shift.id})

        # Generate Barcode
        barcode = self._random_with_N_digits(12)
        values.update({'barcode': str(barcode)})

        is_member = self._is_member_by_plat_number(values.get('plat_number'))

        if is_member:
            _logger.info('Car is member')
            values.update({'trans_type': '1'})  # Member Transaction
            values.update({'entry_member': True})
        else:
            values.update({'trans_type': '0'})  # Casual Transaction
            values.update({'entry_member': False})

        #Set State to Entry
        values.update({'state':'entry'})

        return super(ParkingTransaction, self).create(values)

    def prepare_exit_operator_transaction(self, values):
        parking_booth_obj = self.env['parking.booth']
        parking_shift_obj = self.env['parking.shift']

        # Check Car In Area
        #car_exist = self._check_vehicle(values.get('plat_number'))
        #if not car_exist:
        #    raise ValidationError('Car not exist!')

        # Get Current Shift
        shift = parking_shift_obj.get_current_shift()
        if not shift:
            raise ValidationError('Shift not Found!')
        values.update({'exit_shift_id': shift.id})

        # Fill Exit Date Time
        utc_date = self._local_to_utc("Asia/Jakarta", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        values.update({'exit_datetime': utc_date})

        # Check Member Status
        is_member = self._is_member_by_plat_number(values.get('plat_number'))

        if is_member:
            _logger.info('Car is member')
            values.update({'trans_type': '1'})  # Member Transaction
            values.update({'exit_member': True})
        else:
            values.update({'trans_type': '0'})  # Casual Transaction
            values.update({'exit_member': False})

        # Set State to Entry
        values.update({'state': 'exit'})

        return super(ParkingTransaction, self).write(values)


    @api.one
    def action_entry(self):
        values = {}
        values.update({'state': 'entry'})
        super(ParkingTransaction, self).write(values)

    @api.one
    def trans_close(self):
        values = {}
        values.update({'state': 'done'})
        self.write(values)
    
    def close_by_session(self, session_id):
        sql_req = "UPDATE parking_transaction SET state='done' WHERE session_id=" + str(session_id) + " AND state='exit'"
        self.env.cr.execute(sql_req)

    def calculate_duration(self):
        trans = self
        
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

        values = {}
        values.update({'hours': hours})
        values.update({'minutes': minutes})
        values.update({'seconds': seconds})
        trans.write(values)

    def calculate_general_charge(self):
        trans = self
        pricing_id = trans.pricing_id
        if not pricing_id:
            raise ValidationError('Pricing not Available!')
        
        if pricing_id.state != 'open':
            raise ValidationError('Pricing not allowed!')
                 
        total_amount = 0        

        if not trans.exit_member:
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
        result = self.env['parking.transaction.charging'].create(values)
               
    def calculate_service_charge(self):
        trans = self
        pricing_id = trans.pricing_id
        
        if pricing_id.service_charge > 0:
            if pricing_id.state != 'open':
                raise ValidationError('Pricing not allowed!')
            
            total_amount = 0

            if trans.exit_member:
                if trans.hours > 0 or trans.minutes > 0 or trans.seconds > 0 :                                
                    total_amount = total_amount + pricing_id.service_charge
                    
            values = {}
            values.update({'trans_id': trans.id})
            values.update({'charging_type': 'service'})
            values.update({'total_charging': total_amount})
            result = self.env['parking.transaction.charging'].create(values)
    
    def calculate_missing_charge(self):
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
        
    def calculate_total_amount(self):
        trans = self
        total_amount = 0
        for charging in trans.charging_ids:        
            total_amount = total_amount + charging.total_charging
        
        values = {}
        values.update({'total_amount': total_amount})    
        super(ParkingTransaction,self).write(values)
        
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

    session_id = fields.Many2one('parking.transaction.session', 'Session', readonly=True)
    input_method = fields.Selection(AVAILABLE_INPUT_METHODS, 'Method', required=True)
    plat_number = fields.Char('Plat Number', size=21, readonly=True)
    barcode = fields.Char('Barcode #', size=13, required=True, readonly=True)

    trans_id = fields.Char('Transaction #', size=21, readonly=True)
    sequence_number = fields.Char('Sequence #', size=10, readonly=True)
    card_number = fields.Char('Card Number', size=20, readonly=True)
    card = fields.Char('Card #', size=20)

    trans_type = fields.Selection(AVAILABLE_TRANS_TYPES, 'Transaction Type', size=16, required=True, readonly=True)
    is_manual = fields.Boolean('Is Manual', readonly=True)
    is_pinalty = fields.Boolean('Is Pinalty', readonly=True)

    entry_datetime = fields.Datetime('Entry Date Time', required=True)
    entry_member = fields.Boolean('Entry Member')
    entry_booth_id = fields.Many2one('parking.booth', 'Entry Booth', required=True)
    entry_operator_id = fields.Many2one('hr.employee', 'Entry Operator', required=True)
    entry_driver_id = fields.Many2one('hr.employee', 'Entry Driver')
    entry_shift_id = fields.Many2one('parking.shift', 'Entry Shift', required=True)
    entry_front_image = fields.Binary('Entry Front Image')

    exit_datetime = fields.Datetime('Exit Date Time')
    exit_member = fields.Boolean('Exit Member')
    exit_booth_id = fields.Many2one('parking.booth', 'Exit Booth')
    exit_operator_id = fields.Many2one('hr.employee', 'Exit Operator')
    exit_driver_id = fields.Many2one('hr.employee', 'Exit Driver')
    exit_shift_id = fields.Many2one('parking.shift', 'Exit Shift')
    exit_front_image = fields.Binary('Exit Front Image')

    hours = fields.Float('Hours', readonly=True)
    minutes = fields.Float('Minutes', readonly=True)
    seconds = fields.Float('Seconds', readonly=True)
    pricing_id = fields.Many2one('parking.pricing', 'Pricing')
    casual_charging = fields.Float('Casual Charging', readonly=True)
    service_charging = fields.Float('Service Charging', readonly=True)
    pinalty_charging = fields.Float('Pinalty Charging', readonly=True)
    voucher_charging = fields.Float('Voucher Charging', readonly=True)
    rules_charging = fields.Float('Rules Charging', readonly=True)
    total_amount = fields.Float('Total Charging', readonly=True)

    image_ids = fields.One2many('parking.transaction.image', 'trans_id', 'Images', ondelete='cascade')
    charging_ids = fields.One2many('parking.transaction.charging', 'trans_id', 'Chargings', ondelete='cascade')
    correction_ids = fields.One2many('parking.transaction.correction', 'trans_id', 'Corrections', ondelete='cascade')

    state = fields.Selection(AVAILABLE_STATES, 'Status', size=16, readonly=True, default='draft')

    @api.model
    def create(self, values):

        if 'input_method' in values.keys():
            if values.get('input_method') not in ['0', '1', '2']:
                raise ValidationError('Input Method not define')

            if values.get('input_method') == '0':
                return self.prepare_entry_manless_transaction(values)
            elif values.get('input_method') == '1':
                return self.prepare_entry_operator_transaction(values)
            else:
                return self.prepare_entry_manual_transaction(values)
        else:
            raise ValidationError('Method not Valid')

    @api.multi
    def write(self, values):
        trans = self
        if trans.state == 'done':
            raise ValidationError('Transaction Already Closed!')
        return super(ParkingTransaction, self).write(values)


class ParkingTransactionImage(models.Model):
    _name = "parking.transaction.image"
    _description = "Parking Transaction Image"

    trans_id = fields.Many2one('parking.transaction', 'Transaction ID', readonly=True)
    image = fields.Binary('Image')


class ParkingTransactionCharging(models.Model):
    _name = "parking.transaction.charging"
    _description = "Parking Transaction Charging"

    trans_id = fields.Many2one('parking.transaction', 'Transaction ID', readonly=True)
    charging_type = fields.Selection(AVAILABLE_CHARGING_TYPES, 'Charging Type', required=True, readonly=True)
    total_charging = fields.Float('Total Charging')


class ParkingTransactionCorrection(models.Model):
    _name = "parking.transaction.correction"
    _description = "Parking Transaction Correction"

    trans_id = fields.Many2one('parking.transaction', 'Transaction ID', readonly=True)
    new_trans_id = fields.Many2one('parking.transaction', 'Transaction ID', readonly=True)
    remarks = fields.Text('Remarks')

    
