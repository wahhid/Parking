import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError, Warning

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [    
    ('open','Open'),    
    ('done','Closed'),
]

class ParkingPricing(models.Model):
    _name = "parking.pricing"

    name = fields.char('Name', size=50, required=True),
    image1 = fields.binary('Image'),
    code = fields.char('Code', size=1, required=True),
    vehicle_type_id = fields.many2one('parking.vehicle.type', 'Vechile Type', required=True)
    init_duration = fields.integer('Initial Duration', required=True, default=0)
    first_hour_charge = fields.float('First Hour', required=True, default=0)
    second_hour_charge = fields.float('Second Hour', required=True, default=0)
    third_hour_charge = fields.float('Third Hour', required=True, default=0)
    next_hour_charge = fields.float('Next Hour', required=True, default=0)
    service_charge = fields.float('Service', required=True, default=0)
    pinalty_charge = fields.float('Pinalty', required=True, default=0)
    state = fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True, default='open')
