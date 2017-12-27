import logging

from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)


class hr_employee(osv.osv):
    _name = "hr.employee"
    _inherit = "hr.employee"
    
    def get_trans(self, cr, uid, ids, context=None ):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
        
    _columns = {    
        'is_valet_driver': fields.boolean('Is Valet Driver'),
    }
    
hr_employee()

