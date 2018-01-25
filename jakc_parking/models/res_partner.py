import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp import models, fields, api
from openerp.exceptions import ValidationError, Warning

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


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.one
    def get_car_count(self):
        for partner in self:
            count = 0
            for membership in partner.parking_membership_ids:
                if membership.state == 'open':
                    count += 1
        self.car_count = count

    is_parking_member = fields.Boolean('Is Parking Member')
    is_employee = fields.Boolean('Is Employee')
    parking_membership_ids = fields.One2many('parking.membership', 'res_partner_id', 'Parking Membership')
    car_count = fields.Integer(compute="get_car_count", string='Car #')

class ParkingMembership(models.Model):
    _name = "parking.membership"
    _inherit = ['mail.thread']
    _rec_name = 'plat_number'

    @api.one
    def trans_confirm(self):
        values = {}
        values.update({'state':'open'})
        self.write(values)

    @api.one
    def trans_re_open(self):
        values = {}
        values.update({'state':'open'})
        self.write(values)

    def generate_membership_id(self):
        _logger.info('Start Generate Membership ID')        
        trans_seq_id = self.env['ir.sequence'].get('parking.membership.sequence')
        trans_data = {}
        trans_data.update({'membership_id':trans_seq_id[0]})        
        super(ParkingMembership,self).write(trans_data)
        _logger.info('End Generate Membership ID')

    def _is_car_in_parking_area(self):
        _logger.info('Start Is Car In Parking Area')
        _logger.info('End Is Car In Parking Area')
        
    def _get_last_membership(self):
        _logger.info('Start Get Last Membership')
        
        _logger.info('End Get Last Membership')

    membership_id = fields.Char('Membership #', size=10, readonly=True)
    res_partner_id = fields.Many2one('res.partner', 'Customer', required=True)
    plat_number = fields.Char('Plat Number', size=10, required=True)
    card_number = fields.Char('Card Number', size=20)
    product_id = fields.Many2one('product.product', 'Product')
    membership_payment_ids = fields.One2many('parking.membership.payment', 'parking_membership_id', 'Payments')

    state = fields.Selection(AVAILABLE_STATES, 'Status', readonly=True, default='draft')

    @api.model
    def create(self, values):
        result = super(ParkingMembership,self).create(values)
        result.generate_membership_id()
        return result


class ParkingMembershipPayment(models.Model):
    _name = "parking.membership.payment"


    @api.one
    def trans_create_invoice(self):
        invoice_obj = self.env['account.invoice']
        invoice_line_obj = self.env['account.invoice.line']
        invoice_tax_obj = self.env['account.invoice.tax']
        parking_membership_obj = self.env['parking.membership']
        values = {}
        values.update({'state':'invoiced'})
        trans = self

        # print trans
        partner = trans.parking_membership_id.res_partner_id
        product = trans.parking_membership_id.product_id
        account_id = partner.property_account_receivable_id and partner.property_account_receivable_id.id or False
        fpos_id = partner.property_account_position_id and partner.property_account_position_id.id or False

        # Create Invoice
        invoice_values = {}
        invoice_values.update({'partner_id': partner.id})
        invoice_values.update({'account_id': account_id})
        invoice_values.update({'fiscal_position': fpos_id})
        invoice_id = invoice_obj.create(invoice_values)

        # Update Invoice ID and Status
        self.invoice_id = invoice_id.id

        # Create Invoice Line
        quantity = trans.payment_duration
        account_line_values = {
            'product_id': product.id,
            'quantity': trans.payment_duration,
        }

        line_dict = invoice_line_obj.product_id_change({}, product.id, False, quantity, '', 'out_invoice', partner.id, fpos_id, price_unit=0.0)
        account_line_values.update(line_dict['value'])
        account_line_values['invoice_id'] = invoice_id
        invoice_line_id = invoice_line_obj.create(account_line_values)
        invoice_obj.write({'invoice_line': [(6, 0, [invoice_line_id])]})

    @api.one
    def trans_cancel_invoice(self):
        trans = self

    @api.onchange('parking_membership_id', 'payment_duration', 'start_date')
    def onchange_payment_duration(self):
        if self.parking_membership_id and self.start_date and self.payment_duration > 0:
            self.end_date = datetime.strptime(self.start_date,'%Y-%m-%d') + relativedelta(months=self.payment_duration)
            self.total_amount = self.parking_membership_id.product_id.list_price * self.payment_duration

    parking_membership_id = fields.Many2one('parking.membership', 'Parking Membership', required=True)
    trans_date = fields.Date('Transaction Date', required=True, readonly=True, default=datetime.today())
    payment_duration = fields.Integer('Payment Duration (in month)', required=True, default=1)
    billing_type = fields.Selection([('nobilling','Non Billing'),('billing','Billing')],'Billing Type', default='nobilling', required=True)
    start_date = fields.Date('Start Date', required=True, default=datetime.today())
    end_date = fields.Date('End Date', readonly=True)
    total_amount = fields.Float('Total Payment', readonly=True)
    invoice_id = fields.Many2one('account.invoice', 'Invoice', readonly=True)
    state = fields.Selection(AVAILABLE_MEMBER_STATE, 'State', readonly=True)

    @api.model
    def create(self, values):
        end_date = datetime.today()+ relativedelta(months=values.get('payment_duration'))  
        values.update({'end_date': end_date})
        return super(ParkingMembershipPayment, self).create(values)

    @api.multi
    def write(self, values):
        trans = self
        if trans.state == 'paid':
            raise ValidationError('Transaction Already Paid!')
        
        if 'state' in values.keys():
            if values.get('state') == 'invoiced':
                return self._create_invoice(values)

        if 'payment_duration' in values.keys():
            end_date = datetime.today()+ relativedelta(months=values.get('payment_duration'))  
            values.update({'end_date': end_date})        
        return super(ParkingMembershipPayment, self).write(values)

