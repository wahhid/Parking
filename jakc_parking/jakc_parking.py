import logging
from datetime import datetime
from decimal import Decimal
from pytz import timezone

from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [
    ('draft','Draft'),
    ('open','Open'),
    ('done','Close'),
]

class parking_vehicle_type(osv.osv):
    _name = "parking.vehicle.type"
    _description = "Parking Vehicle Type"
    _columns = {
        'name': fields.char('Name', size=100, required=True),
        'state': fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),
    }
    _defaults = {
        'state': lambda  *a: 'open',
    }
parking_vehicle_type()


class parking_shift(osv.osv):
    _name = "parking.shift"
    _description = "Parking Shift"
    
    def get_trans(self, cr, uid, ids, context=None):
        trans_id  = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    def get_active_trans(self, cr, uid, context=None):
        args = {'state','=','open'} 
        ids = self.search(cr, uid, args, context=context)
        return self.browse(cr, uid, ids, context=context)
    
    def _convert_time_to_str(self, cr, uid, float_time, context=None):
        str_float_time  = str(float_time)
        dict_float_time = str_float_time.split(".")
        hour = dict_float_time[0].zfill(2)
        minutes = str(Decimal(float(str_float_time)) % 1 * 60).replace(".","").zfill(2)[:2]
        return hour + ":"  + minutes
            
    def get_current_shift(self, cr, uid, context=None):
        current_shift = False        
        tzinfo = timezone('Asia/Jakarta')
        shift_ids = self.search(cr, uid, [], context=context)
        shifts = self.browse(cr, uid, shift_ids, context=context)        
        str_now = datetime.now(timezone("Asia/Jakarta"))
        #str_now = datetime.now()                                
        _logger.info("Now : "  + str_now.strftime('%Y-%m-%d %H:%M:%S'))
        for shift in shifts:
            #Convert Start Time to String
            str_start_time = self._convert_time_to_str(cr, uid, shift.start_time, context)
            #Convert End Time to String
            str_end_time = self._convert_time_to_str(cr, uid, shift.end_time, context)                                
            shift_start = str_now.strftime('%Y-%m-%d') + " " + str_start_time + ":00"
            _logger.info("Shift Start : " + shift_start)            
            shift_end = str_now.strftime('%Y-%m-%d') + " " + str_end_time + ":00"
            _logger.info("Shift End : " + shift_end)            
            
            start_datetime = tzinfo.localize(datetime.strptime(shift_start,'%Y-%m-%d %H:%M:%S'))
            end_datetime = tzinfo.localize(datetime.strptime(shift_end,'%Y-%m-%d %H:%M:%S'))
            
            #start_datetime = datetime.strptime(shift_start,'%Y-%m-%d %H:%M:%S')
            #end_datetime = datetime.strptime(shift_end,'%Y-%m-%d %H:%M:%S')            

            if str_now > start_datetime and str_now < end_datetime:
                current_shift = shift                
                break
        return current_shift
        
    _columns = {
        'name': fields.char('Name', size=100, required=True),
        'start_time': fields.float('Start Time', required=True),
        'end_time': fields.float('End Time', required=True),
        'next_day': fields.boolean('Next Day'),
        'state': fields.selection(AVAILABLE_STATES,size=16),
    }
    
    _defaults = {
        'next_day': lambda *a: False,
        'state': lambda *a: 'open',
    }
parking_shift()
