import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [    
    ('draft','New'),                
    ('open','Open'),    
    ('done','Closed'),
]

AVAILABLE_MEMBER_STATE = [
    ('none', 'Non Member'),
    ('canceled', 'Cancelled Member'),
    ('old', 'Old Member'),
    ('expired', 'Expired'),
    ('waiting', 'Waiting Member'),
    ('invoiced', 'Invoiced Member'),
    ('free', 'Free Member'),
    ('paid', 'Paid Member'),
]


class res_partner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    _columns = {        
        'is_parking_member': fields.boolean('Is Parking Member'),        
        'is_employee': fields.boolean('Is Employee'),
        'parking_membership_ids': fields.one2many('parking.membership','res_partner_id', 'Parking Membership'),        
    }             
res_partner()
    

class parking_membership(osv.osv):
    _name = "parking.membership"
    _inherit = ['mail.thread']
    
    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    def trans_confirm(self, cr, uid, ids, context=None):
        values = {}
        values.update({'state':'open'})
        return self.write(cr, uid, ids, values, context=context)        
    
    def trans_re_open(self, cr, uid, ids, context=None):
        values = {}
        values.update({'state':'open'})
        return self.write(cr, uid, ids, values, context=context)    
    
    def _confirm(self, cr, uid, ids, values, context=None):
        return super(parking_membership, self).write(cr, uid, ids, values, context=context)
    
    def _re_open(self, cr, uid, ids, values, context=None):
        return super(parking_membership, self).write(cr, uid, ids, values, context=context)
    
    def _generate_membership_id(self, cr, uid, ids, context=None):
        _logger.info('Start Generate Membership ID')        
        trans_seq_id = self.pool.get('ir.sequence').get(cr, uid, 'parking.membership.sequence'),            
        trans_data = {}
        trans_data.update({'membership_id':trans_seq_id[0]})        
        super(parking_membership,self).write(cr, uid, ids, trans_data, context=context)
        _logger.info('End Generate Membership ID')

    def _is_car_in_parking_area(self, cr, uid, context=None):
        _logger.info('Start Is Car In Parking Area')
        _logger.info('End Is Car In Parking Area')
        
    def _get_last_membership(self, cr, uid, context=None):
        _logger.info('Start Get Last Membership')
        
        _logger.info('End Get Last Membership')
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):            
            name = record.res_partner_id.name + " (" + record.plat_number + ")"
            res.append((record.id, name))
        return res        

             
    #def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
    #    if args is None:
    #        args = []
    #    if context is None:
    #        context = {}
    #    ids = []
    #    if name:
    #        ids = self.search(cr, uid, [('name', 'ilike', name)] + args, limit=limit)
    #    if not ids:
    #        ids = self.search(cr, uid, [('membership_id', 'ilike', name)] + args, limit=limit)
    #        
    #    return self.name_get(cr, uid, ids, context=context)
                        
    _columns = {               
        'membership_id': fields.char('Membership #', size=10 , readonly= True),
        'res_partner_id': fields.many2one('res.partner','Customer', required=True),
        'plat_number': fields.char('Plat Number', size=10, required=True),
        'card_number': fields.char('Card Number', size=20),        
        'product_id': fields.many2one('product.product','Product'),
        'membership_payment_ids': fields.one2many('parking.membership.payment','parking_membership_id', 'Payments'),
        'state': fields.selection(AVAILABLE_STATES,'Status', readonly=True),                                 
    }
    
    _defaults = {
        'state': lambda *a: 'draft',
    }
    
    def create(self, cr, uid, values, context=None):
        #Create Membership
        result = super(parking_membership,self).create(cr, uid, values, context=context)
        #Generate Membership ID
        self._generate_membership_id(cr, uid, [result], context)
        return result
    
    def write(self, cr, uid, ids, values, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)
                
        if 'state' in values.keys():
            if values.get('state') == 'open':
                return self._confirm(cr, uid, ids, values, context=context)
        
        return super(parking_membership,self).write(cr, uid, ids, values, context=context)
                
parking_membership()
    
class parking_membership_payment(osv.osv):
    _name = "parking.membership.payment"

    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    def trans_create_invoice(self,cr, uid, ids, context=None):
        print "Invoice ID : " + str(ids[0])
        values = {}
        values.update({'state':'invoiced'})        
        self._create_invoice(cr, uid, ids, values, context=context)
        
    def trans_cancel_invoice(self,cr, uid, ids, context=None):
        trans_id = ids[0]
        
    def _create_invoice(self, cr, uid, ids, values, context=None):
        
        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        invoice_tax_obj = self.pool.get('account.invoice.tax')
        parking_membership_obj = self.pool.get('parking.membership')
        
        if type(ids) in (int, long,):
            ids = [ids]
            
        trans = self.get_trans(cr, uid, ids, context=context)
        if not trans:
            raise osv.except_osv(('Warning'), ('Parking Membership Payment Error!'))
            
        #print trans 
        partner = trans.parking_membership_id.res_partner_id
        product = trans.parking_membership_id.product_id
        account_id = partner.property_account_receivable and partner.property_account_receivable.id or False
        fpos_id = partner.property_account_position and partner.property_account_position.id or False
        
        #Create Invoice
        invoice_values = {}
        invoice_values.update({'partner_id': partner.id})
        invoice_values.update({'account_id': account_id})
        invoice_values.update({'fiscal_position': fpos_id})        
        invoice_id = invoice_obj.create(cr, uid, invoice_values, context=context)
                
        #Update Invoice ID and Status
        values.update({'invoice_id': invoice_id})
        super(parking_membership_payment,self).write(cr, uid, ids, values, context=context)        
        
        #Create Invoice Line
        quantity = trans.payment_duration
        account_line_values =  {
                'product_id': product.id,
                'quantity': trans.payment_duration,
            }
        
        line_dict = invoice_line_obj.product_id_change(cr, uid, {}, product.id, False, quantity, '', 'out_invoice', partner.id, fpos_id, price_unit=0.0, context=context)
        account_line_values.update(line_dict['value'])
        account_line_values['invoice_id'] = invoice_id
        invoice_line_id = invoice_line_obj.create(cr, uid, account_line_values, context=context)
        invoice_obj.write(cr, uid, invoice_id, {'invoice_line': [(6, 0, [invoice_line_id])]}, context=context)
        
        return True            
        
    def _get_membership_state(self, cr, uid, ids, name, args, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)        
        res = {}
        for id in ids:            
            res[id] = 'none'
        for id in ids:
            invoice_id = trans.invoice_id            
            invoice_state = invoice_id.state
            if invoice_state == 'paid':
                res[id] = 'paid'        
            if invoice_state == 'open':
                res[id] = 'invoiced'
            if invoice_state == 'cancel':
                res[id] = 'canceled'
            if invoice_state == 'draft' or invoice_state == 'proforma':
                res[id] = 'waiting'                        
        return res
    
    def onchange_payment_duration(self, cr, uid, ids, payment_duration=False):        
        if not payment_duration:
            return {'value': {'end_date': False}}
        end_date = datetime.today()+ relativedelta(months=payment_duration)        
        return {'value': {'end_date': end_date.strftime('%Y-%m-%d')}}

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):            
            name = "Payment For " + " " + record.parking_membership_id.membership_id 
            res.append((record.id, name))
        return res  
    

    #def name_get(self, cr, uid, ids, context=None):
    #    trans = self.get_trans(cr, uid, ids, context=context)
    #    res = []
    #    name = "Payment for " + trans.parking_membership_id.membership_id
    #    res.append((trans.id, name))
    #    return res               
                    
    _columns = {
        'parking_membership_id': fields.many2one('parking.membership','Parking Membership', required=True),
        'trans_date': fields.date('Transaction Date', required=True, readonly=True),
        'payment_duration': fields.integer('Payment Duration (in month)'),
        'start_date': fields.date('Start Date', readonly=True),
        'end_date': fields.date('End Date', readonly=True),        
        'total_amount': fields.float('Total Payment', readoly=True),        
        'invoice_id': fields.many2one('account.invoice', 'Invoice', readonly=True),
        'invoice_state': fields.function(_get_membership_state,string = 'Invoice Status', type = 'selection',selection = AVAILABLE_MEMBER_STATE),
        'state': fields.function(_get_membership_state,string = 'Status', type = 'selection',selection = AVAILABLE_MEMBER_STATE),                                   
    }    
    
    _defaults = {        
        'trans_date': fields.date.context_today,
        'payment_duration': lambda *a: 1, 
        'start_date': fields.date.context_today,                      
        'state': lambda *a: 'none',
    }
    
    def create(self, cr, uid, values, context=None):
        
        end_date = datetime.today()+ relativedelta(months=values.get('payment_duration'))  
        values.update({'end_date': end_date})
        return super(parking_membership_payment, self).create(cr, uid, values, context=context)
        
    def write(self, cr, uid, ids, values, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)        
        if trans.state == 'paid':
            raise osv.except_osv(('Warning'), ('Transaction Already Paid!'))
        
        if 'state' in values.keys():
            if values.get('state') == 'invoiced':
                return self._create_invoice(cr, uid, ids, values, context=context)

        if 'payment_duration' in values.keys():
            end_date = datetime.today()+ relativedelta(months=values.get('payment_duration'))  
            values.update({'end_date': end_date})        
        return super(parking_membership_payment, self).write(cr, uid, ids, values, context=context)
                            
parking_membership_payment()
