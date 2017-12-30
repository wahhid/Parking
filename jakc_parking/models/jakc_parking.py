import logging
from datetime import datetime
from decimal import Decimal
from pytz import timezone

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [
    ('draft','Draft'),
    ('open','Open'),
    ('done','Close'),
]


class ParkingVehicleType(models.Model):
    _name = "parking.vehicle.type"
    _description = "Parking Vehicle Type"

    name = fields.Char('Name', size=100, required=True)
    state = fields.Selection(AVAILABLE_STATES,'Status', size=16, readonly=True, default='open')


class ParkingShift(models.Model):
    _name = "parking.shift"
    _description = "Parking Shift"

    def get_active_trans(self):
        args = {'state','=','open'} 
        parking_shift_ids = self.search(args)
        if len(parking_shift_ids)>0:
            return parking_shift_ids[0]
        else:
            return False

    def _convert_time_to_str(self, float_time):
        str_float_time  = str(float_time)
        dict_float_time = str_float_time.split(".")
        hour = dict_float_time[0].zfill(2)
        minutes = str(Decimal(float(str_float_time)) % 1 * 60).replace(".","").zfill(2)[:2]
        return hour + ":" + minutes

    def get_current_shift(self):
        current_shift = False        
        tzinfo = timezone('Asia/Jakarta')
        shift_ids = self.search([])
        str_now = datetime.now(timezone("Asia/Jakarta"))
        #str_now = datetime.now()                                
        _logger.info("Now : "  + str_now.strftime('%Y-%m-%d %H:%M:%S'))
        for shift in shift_ids:
            #Convert Start Time to String
            str_start_time = self._convert_time_to_str(shift.start_time)
            #Convert End Time to String
            str_end_time = self._convert_time_to_str(shift.end_time)
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

    name = fields.Char('Name', size=100, required=True)
    start_time = fields.Float('Start Time', required=True)
    end_time = fields.Float('End Time', required=True)
    next_day = fields.Boolean('Next Day', default=False)
    state = fields.Selection(AVAILABLE_STATES,size=6, readonly=True, default='open')