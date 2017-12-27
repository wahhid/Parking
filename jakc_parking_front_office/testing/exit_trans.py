import base64
import os
import pytz
import xmlrpclib
from datetime import datetime

from escpos import *

file_path = '/home/wahhid/fswebcam'
local_tz = pytz.timezone('Asia/Jakarta') 
user = 'admin'
pwd = 'P@ssw0rd'
dbname = 'park_dev'
server = 'localhost'
port = '8069'
booth_id = 3

sock = xmlrpclib.ServerProxy('http://' + server + ':' + port +'/xmlrpc/common')
uid = sock.login(dbname , user , pwd)
sock = xmlrpclib.ServerProxy('http://' + server + ':' + port + '/xmlrpc/object')

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary

def print_receipt(trans_id, date_time_in, operator_in_id, booth_in_id):
    try:
        Epson = printer.Serial("/dev/ttyS0")
        Epson.text("MAL TAMAN ANGGREK\n")    
        Epson.text("Booth : " + booth_in_id[1] + "\n")
        Epson.text("Operator : " + operator_in_id[1] + "\n")    
        Epson.barcode(trans_id,'EAN13',64,2,'','')
        Epson.cut()
    except:
        print "Error"
    else:
        print "Print Receipt"

def capture_picture(trans_id):
    try:
        os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save ' + file_path +'/' + trans_id + '.jpg')            
    except:
        print "Error"
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
    sock.execute(dbname, uid, pwd, 'ir.attachment', 'create', values)
    print "Upload Image"
    

def create():
    trans_id = input("Barcode : ")

    sock = xmlrpclib.ServerProxy('http://' + server + ':' + port +'/xmlrpc/common')
    uid = sock.login(dbname , user , pwd)

    sock = xmlrpclib.ServerProxy('http://' + server + ':' + port + '/xmlrpc/object')
    args = [('trans_id','=', str(trans_id)),('state','=','entry')]
    ids = sock.execute(dbname, uid, pwd, 'park.trans', 'search',  args)
    if ids:
        print "Vehicle Exist"
        booth_pricing_args = [('booth_id','=',booth_id)]    
        pricing_ids = sock.execute(dbname, uid, pwd, 'park.booth.pricing', 'search', booth_pricing_args)    
        pricings = sock.execute(dbname, uid, pwd, 'park.booth.pricing', 'read', pricing_ids, [])
        print pricings
        pricing_id = input("Pricing ID : ")        
        values = {}
        values.update({'date_time_out': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')})
        values.update({'operator_out_id': 1})
        values.update({'shift_out_id': 1})
        values.update({'booth_out_id': booth_id})
        values.update({'pricing_id': pricing_id})
        values.update({'state':'exit'})    
        result = sock.execute(dbname, uid, pwd, 'park.trans', 'write', ids, values)
        print "Process Success"        
        values = {}
        values.update({'state':'done'})
        result = sock.execute(dbname, uid, pwd, 'park.trans', 'write', ids, values)
        capture_picture(str(trans_id))
        upload_image(ids[0], str(trans_id))        
        print "Transaction Closed"
    else:
        print "Vehicle not Exist"
        
create()


