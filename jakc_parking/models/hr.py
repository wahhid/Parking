import logging

from odoo import models, fields, osv
from odoo.exceptions import ValidationError, Warning

_logger = logging.getLogger(__name__)


class HrEmployee(osv.osv):
    _inherit = "hr.employee"

    'is_valet_driver': fields.Boolean('Is Valet Driver')
