import base64
import os
import pytz

from escpos import *
from lib.park_openerp import park

file_path = '/home/wahhid/fswebcam'
local_tz = pytz.timezone('Asia/Jakarta') 
user = 'admin'
pwd = 'P@ssw0rd'
dbname = 'park_dev'
server = 'localhost'
port = '8069'
booth_id = 1

park_openerp = park(server,port,dbname,user,pwd)
status, message = park_openerp.auth()


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary

def print_receipt(trans_id, date_time_in, operator_in_id, booth_in_id):
    try:
        Epson = printer.Serial("/dev/ttyUSB0")
        #0557:2008
        #Epson = printer.Usb(0x0557,0x2008)
        Epson.text("MAL TAMAN ANGGREK\n")    
        Epson.text("Booth : " + booth_in_id[1] + "\n")
        Epson.text("Operator : " + operator_in_id[1] + "\n")        
        Epson.barcode(trans_id,'EAN13',64,2,'','')
        Epson.text("\n")
        Epson.text("\n")
        Epson.text("\n")
        Epson.text("\n")
        Epson.text("\n")        
        Epson.cut()
    except:
        print "Error Print"
    else:
        print "Print Receipt"

def capture_picture(trans_id):
    try:
        os.system('fswebcam -r 640x480  -S 3 --jpeg 50 --save ' + file_path +'/' + trans_id + '.jpg')            
    except:
        print "Error Capture"
    else:
        print "Capture Picture"

def upload_image(id,trans_id):
    file = open(file_path +'/' + trans_id + '.jpg', "rb")  
    data = file.read()  
    file.close()  
    byte_arr = base64.b64encode(data)
    values = {}
    values.update({'name': trans_id + '.jpg'})
    values.update({'datas_fname': trans_id + '.jpg'})
    values.update({'park_trans_id': id})    
    values.update({'type': 'binary'})
    values.update({'datas': byte_arr})
    #sock.execute(dbname, uid, pwd, 'ir.attachment', 'create', values)
    print "Upload Image"
    

def create():
        
    values = {}
    values.update({'vehicle_type_id': 1})
    values.update({'booth_in_id': 1})
    values.update({'operator_in_id': 1})    
    values.update({'shift_in_id': 1})
    values.update({'state': 'entry'})

    result, message = park_openerp.create_parking_transaction(values)
    #id = sock.execute(dbname, uid, pwd, 'park.trans', 'create', values)

    #args = [('id','=',id)]
    #ids = sock.execute(dbname, uid, pwd, 'park.trans', 'search', args)
    #fields = []
    #data = sock.execute(dbname, uid, pwd, 'park.trans', 'read', ids, fields)

    #trans_data = data[0]
    #trans_id = trans_data.get('trans_id')
    #print trans_data.get('trans_id')
    #print trans_data.get('shift_in_id')[1]
    #utc = datetime.strptime(trans_data.get('date_time_in'),'%Y-%m-%d %H:%M:%S')
    #print utc_to_local(utc).strftime('%Y-%m-%d %H:%M:%S')
    #print trans_data.get('operator_in_id')[1]
    #print trans_data.get('booth_in_id')[1]

    #Capture Image
    #capture_picture(trans_id)
    #Upload Image
    #upload_image(id,trans_id)
    #Print Receipt
    #print_receipt(trans_data.get('trans_id'), utc_to_local(utc).strftime('%Y-%m-%d %H:%M:%S'), trans_data.get('shift_in_id'), trans_data.get('booth_in_id'))

create()