import logging

from odoo import models, fields, osv
from odoo.exceptions import ValidationError, Warning

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_valet_driver = fields.Boolean('Is Valet Driver')
