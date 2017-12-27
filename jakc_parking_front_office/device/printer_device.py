import pytz
from datetime import datetime

from escpos import escpos
from escpos import printer


class Printer_device:
    
    def __init__(self, parent, ip_address=None, port='/dev/ttyUSB0', printer_type=0):        
        self.parent = parent
        self.park_openerp = self.parent.park_openerp
        self.booth = self.parent.booth
        self.operator = self.parent.operator 

        self.port = port
        self.printer_type = printer_type
        self.ip_address = ip_address
        
    def connect(self):
        try:
            if self.printer_type == 0:
                print "Try connect to printer " + self.port
                self.Epson = printer.Serial(self.port)
                return True, "Printer Connected to " + self.port
            if self.printer_type == 1:
                print "Try connect to printer " + self.ip_address
                self.Epson = printer.Network(self.ip_address)
                return True, "Printer Connected to " + self.ip_address            
        except escpos.Error as e:     
            print e       
            return False, e
        
        
    def _utc_to_local(self, timezone, current_date):        
        tzinfo_local = pytz.timezone(timezone)        
        tzinfo_utc = pytz.timezone("UTC")        
        utc_date = tzinfo_utc.localize(current_date, is_dst=None)
        local_date = utc_date.astimezone(tzinfo_local)
        return local_date
    
    def _local_to_utc(self, timezone, str_datetime):
        tzinfo = pytz.timezone(timezone)
        utc_datetime = datetime.strptime(str_datetime,'%Y-%m-%d %H:%M:%S')
        local_datetime = tzinfo.localize(utc_datetime, is_dst=None)
        utc = local_datetime.astimezone(pytz.utc)
        return utc
        
    
    def print_entry_receipt(self, trans):
        self.Epson.control("FF")
        self.Epson.control("FF")
        self.Epson.control("FF")
        self.Epson.control("FF")
        self.Epson.control("FF")
        self.Epson.set("center", "A", "", 1.5, 2)
        self.Epson.text("Mal Taman Anggrek\n")
        self.Epson.set("center", "A", "", 1, 1)
        self.Epson.text("Dunia Anda\n")
        if self.printer_type == 0:                
            self.Epson.text(trans['trans_id'] + "\n")
        if self.printer_type == 1:
            self.Epson.barcode(trans['barcode'],'EAN13',64,2,'','')
        self.Epson.text("\n")        
        self.Epson.set("left", "A", "", 1, 1)
        self.Epson.text("Plat Number : " + trans['plat_number'] + "\n")
        booth = self.park_openerp.get_booth(trans['entry_booth_id'][0])[0]
        self.Epson.text("Booth       : " +  "(" + booth['code'] + ")" + booth['name'] + "\n")
        entry_datetime = self._utc_to_local("Asia/Jakarta", datetime.strptime(trans['entry_datetime'],"%Y-%m-%d %H:%M:%S"))
        str_entry_datetime = entry_datetime.strftime("%d-%m-%Y %H:%M:%S")                
        self.Epson.text("Entry Time  : " + str_entry_datetime + "\n")
        operator = self.park_openerp.get_operator(trans['entry_operator_id'][0])[0]
        self.Epson.text("Operator    : " + operator['name'] + "\n")        
        self.Epson.text("\n")
        self.Epson.text("\n")        
        self.Epson.text("\n")        
        self.Epson.cut()
        
    def print_exit_reciept(self ,trans):
        self.Epson.control("FF")
        self.Epson.control("FF")
        self.Epson.control("FF")
        self.Epson.control("FF")
        self.Epson.control("FF")
        self.Epson.control("FF")
        self.Epson.control("FF")        
        self.Epson.set("center", "A", "", 1.5, 2)
        self.Epson.text("Mal Taman Anggrek\n")
        self.Epson.set("center", "A", "", 1, 1)
        self.Epson.text("Dunia Anda\n")        
        self.Epson.text(trans['trans_id'] + "\n")
        self.Epson.text("\n")
        self.Epson.set("left", "A", "", 1, 1)        
        self.Epson.text("Plat Number : " + trans['plat_number'] + "\n")
        
        if trans['trans_type'] == '0':
            trans_type = 'Casual'
        elif trans['trans_type'] == '1':
            trans_type = 'Manual'
        elif trans['trans_type'] == '2':
            trans_type = 'Pinalty'
        else:
            trans_type = '-'                
        self.Epson.text("Trans Type  : " + trans_type + "\n")                            
        self.Epson.text("Pricing     : " + trans['pricing_id'][1] + "\n")        
        booth = self.park_openerp.get_booth(trans['exit_booth_id'][0])[0]
        self.Epson.text("Booth       : " +  "(" + booth['code'] + ")" + booth['name'] + "\n")        
        entry_datetime = self._utc_to_local("Asia/Jakarta", datetime.strptime(trans['entry_datetime'],"%Y-%m-%d %H:%M:%S"))
        str_entry_datetime = entry_datetime.strftime("%d-%m-%Y %H:%M:%S")                
        self.Epson.text("Entry Time  : " + str_entry_datetime + "\n")
        exit_datetime = self._utc_to_local("Asia/Jakarta", datetime.strptime(trans['exit_datetime'],"%Y-%m-%d %H:%M:%S"))
        str_exit_datetime = exit_datetime.strftime("%d-%m-%Y %H:%M:%S")                        
        self.Epson.text("Exit Time   : " + str_exit_datetime + "\n")
        operator = self.park_openerp.get_operator(trans['exit_operator_id'][0])[0]
        self.Epson.text("Operator    : " + operator['name'] + "\n") 
        self.Epson.text("Duration    : " + str(trans['hours']) + ":" + str(trans['minutes']) + ":" + str(trans['seconds']) + "\n")
        self.Epson.text("Total       : " + str(trans['total_amount']) + "\n")             
        self.Epson.text("\n")
        self.Epson.text("\n")        
        self.Epson.text("\n")        
        self.Epson.cut()
                