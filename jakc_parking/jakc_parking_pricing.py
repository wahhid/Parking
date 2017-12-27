import logging

from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [    
    ('open','Open'),    
    ('done','Closed'),
]

class parking_pricing(osv.osv):
    _name = "parking.pricing"
    _columns = {
        'name': fields.char('Name', size=50, required=True),
        'image1': fields.binary('Image'),
        'code': fields.char('Code', size=1, required=True),
        'vehicle_type_id': fields.many2one('parking.vehicle.type','Vechile Type', required=True),
        'init_duration': fields.integer('Initial Duration', required=True),
        'first_hour_charge': fields.float('First Hour', required=True),
        'second_hour_charge': fields.float('Second Hour', required=True),
        'third_hour_charge': fields.float('Third Hour', required=True),
        'next_hour_charge': fields.float('Next Hour', required=True),
        'service_charge': fields.float('Service', required=True),
        'pinalty_charge': fields.float('Pinalty', required=True),        
        'state': fields.selection(AVAILABLE_STATES,'Status', size=16, readonly=True),
    }
    _defaults = {
        'init_duration': lambda *a: 0,
        'first_hour_charge': lambda *a: 0,
        'second_hour_charge': lambda *a: 0,
        'third_hour_charge': lambda *a: 0,
        'next_hour_charge': lambda *a: 0,
        'service_charge': lambda *a: 0,
        'pinalty_charge': lambda *a: 0,
        'state': lambda*a: 'open',                
    }
    
parking_pricing()
