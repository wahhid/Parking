import logging

from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [    
    ('open','Open'),    
    ('reopen','Re-Open'),
    ('done','Closed'),
]

AVAILABLE_PRINTER_STATES = [
    ('enable', 'Enable'),
    ('disable', 'Disable'),
]

AVAILABLE_CAMERA_STATES = [
    ('enable', 'Enable'),
    ('disable', 'Disable'),
]

AVAILABLE_BOOTH_TYPES = [
    ('0','Booth In'),
    ('1','Booth Out'),
    ('2','Booth In and Out'),
]

AVAILABLE_CAMERA_TYPES = [
    ('local','Local Camera'),
    ('network','Network Camera'),    
]

AVAILABLE_PRINTER_TYPES = [
    ('local','Local Printer'),
    ('network','Network Printer'),    
]

AVAILABLE_CAMERA_POSITIONS = [
    ('0', 'Vehicle Camera'),    
    ('1', 'Driver Camera')
]

class parking_booth(osv.osv):
    _name = "parking.booth"
    
    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    def trans_close(self, cr, uid, ids, context=None):
        values = {}
        values.update({'state':'done'})
        self.write(cr, uid, ids, values, context=context)
    
    def trans_re_open(self, cr, uid, ids, context=None):
        values = {}
        values.update({'state':'reopen'})
        self.write(cr, uid, ids, values, context=context)
    
    def close(self, cr, uid, ids, values, context=None):
        return super(parking_booth, self).write(cr, uid, ids, values, context=context)
    
    def reopen(self, cr, uid, ids, values, context=None):
        values.update({'state':'open'})
        return super(parking_booth, self).write(cr, uid, ids, values, context=context)
        
    def _sequence_increment(self, cr, uid, ids, context=None):
        booth = self.get_trans(cr, uid, ids, context=context)
        sequence_number = booth.sequence_number
        values = {}
        values.update({'sequence_number': sequence_number+1})
        super(parking_booth, self).write(cr, uid, ids, values, context=context)
        return sequence_number
        
              
    def generate_sequence_number(self, cr, uid, ids, context=None):
        booth = self.get_trans(cr, uid, ids, context=context)
        sequence_number = self._sequence_increment(cr, uid, ids, context=context)
        return str(sequence_number).zfill(booth.sequence_length)                
                    
        
    _columns = {
        'name': fields.char('Name',size=50, required=True),
        'code': fields.char('Code',size=4, required=True),
        'booth_type': fields.selection(AVAILABLE_BOOTH_TYPES, 'Type', size=16, required=True),
        'is_manless': fields.boolean('Is Manless'),
        'is_driver': fields.boolean('Driver Required'),
        'is_barcode': fields.boolean('Barcode Required'),
        'is_card': fields.boolean('Card Required'),
        'manless_port': fields.char('Manless Port', size=50),
        'printer_state': fields.selection(AVAILABLE_PRINTER_STATES,'Printer Status', size=16),
        'printer_type': fields.selection(AVAILABLE_PRINTER_TYPES, 'Printer Type', size=16),
        'printer_port': fields.char('Printer Port', size=50),
        'printer_ip': fields.char('Printer Ip Address', size=50),
        'printer_ip_port': fields.char('Printer Ip Port', size=50),
        'booth_pricing_ids': fields.one2many('parking.booth.pricing','booth_id','Pricings'),
        'booth_camera_ids': fields.one2many('parking.booth.camera','booth_id','Cameras'),
        'with_sequence': fields.boolean('Sequence Enable'),
        'sequence_number': fields.integer('Sequence #'),
        'sequence_length': fields.integer('Sequence Length'),       
        'state': fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),
    }
    
    _defaults = {
        'is_manless': lambda *a: False,
        'is_driver': lambda *a: False,
        'is_barcode': lambda *a: False,
        'printer_state': lambda *a: 'disable',
        'manless_port': lambda *a: '/dev/ttyUSB0',
        'printer_type': lambda *a: 'local',
        'printer_port': lambda *a: '/dev/ttyS0',        
        'with_sequence': lambda *a: False,
        'sequence_number': lambda *a: 0,
        'sequence_length': lambda *a: 5,
        'state': lambda *a: 'open',        
    }
    
    def create(self, cr, uid, values, context=None):
        return super(parking_booth, self).create(cr, uid, values, context=context)
    
    def write(self, cr, uid, ids, values, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)
        
        if not trans:
            raise osv.except_osv(('Error'), ('Transaction not Found!'))
                
        if trans.state == 'done':  
            if 'state' in values.keys(): #By Pass State
                if values.get('state')  not in ('reopen'):
                    raise osv.except_osv(('Warning'),   ('Transaction Already Closed!'))                
        
        if 'state' in values.keys():
            if values.get('state') == 'done':
                return self.close(cr, uid, ids, values, context=context)
            
            if values.get('state') == 'reopen':                
                return self.reopen(cr, uid, ids, values, context=context)
             
        
        return super(parking_booth, self).write(cr, uid, ids, values, context=context) 
        
parking_booth()

class parking_booth_pricing(osv.osv):
    _name = "parking.booth.pricing"
    
    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    def trans_set_default(self, cr, uid, ids, context=None):
        values = {}
        values.update({'is_default': True})
        return self.write(cr, uid, ids, values, context=context)
        
    def _get_default_booth_pricing(self, cr, uid, context=None):
        args = [('is_default','=',True)]
        ids = self.search(cr, uid, args, context=context)
        if ids:
            booth_pricing = self.browse(cr, uid, ids[0], context=context)
            return booth_pricing
        else:
            return False

    def _enable_default_booth_pricing(self, cr, uid, ids, context=None):
        values = {}
        values.update({'is_default': True})
        return super(parking_booth_pricing,self).write(cr, uid, ids, values, context=context)

                
    def _disable_default_booth_pricing(self, cr, uid, ids, context=None):        
        values = {}
        values.update({'is_default': False})
        return super(parking_booth_pricing,self).write(cr, uid, ids, values, context=context)
                                     
    _columns = {
        'booth_id': fields.many2one('parking.booth', 'Booth', required=True),
        'pricing_id': fields.many2one('parking.pricing', 'Pricing', required=True),
        'is_default': fields.boolean('Is Default'),            
    }
    
    _defaults = {
        'is_default': lambda *a: False,
    }

    def create(self, cr, uid, values, context=None):
        if 'is_default' in values.keys():
            if values.get('is_default'):
                old_default = self._get_default_booth_pricing(cr, uid, context=context)
                if old_default:
                    self._disable_default_booth_pricing(cr, uid, [old_default.id], context=context)
                                                
        return super(parking_booth_pricing, self).create(cr, uid, values, context=context)
                    
    def write(self, cr, uid, ids, values, context=None):
        if 'is_default' in values.keys():
            if values.get('is_default'):
                old_default = self._get_default_booth_pricing(cr, uid, context=context)
                if old_default:
                    self._disable_default_booth_pricing(cr, uid, [old_default.id], context=context)
        
        return super(parking_booth_pricing, self).write(cr, uid, ids, values, context=context)
        
parking_booth_pricing()


class parking_booth_camera(osv.osv):
    _name = "parking.booth.camera"
    
    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    _columns = {
        'booth_id': fields.many2one('parking.booth', 'Booth', required=True),
        'camera_type': fields.selection(AVAILABLE_CAMERA_TYPES, 'Camera Type', size=16, required=True),
        'camera_state': fields.selection(AVAILABLE_CAMERA_STATES, 'Camera Status', size=16),
        'camera_position': fields.selection(AVAILABLE_CAMERA_POSITIONS,'Camera Position', size=20, required=True),
        'camera_device': fields.char('Camera Device', size=50),
        'camera_ip_address': fields.char('Camera Ip Address', size=50),
        'camera_ip_port': fields.char('Camera Ip Port', size=10),
        'state': fields.selection(AVAILABLE_CAMERA_STATES,'Status', size=16),                 
    }
    _defaults = {
        'camera_type': lambda *a: 'local',
        'camera_state': lambda *a: 'disable',
        'camera_device': lambda *a: '/dev/video0',
    }

parking_booth_camera()