import base64
import os
import xmlrpclib
from datetime import datetime

file_path = '/home/wahhid/fswebcam'

def capture_picture(trans_id):
    try:
        os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save ' + file_path +'/' + trans_id + '.jpg')            
    except:
        print "Error"
    else:
        print "Capture Picture"
    
    
user = 'admin'
pwd = 'P@ssw0rd'
dbname = 'park_dev'
server = 'localhost'
port = '8069'
booth_id = 1

sock = xmlrpclib.ServerProxy('http://' + server + ':' + port +'/xmlrpc/common')
uid = sock.login(dbname , user , pwd)
sock = xmlrpclib.ServerProxy('http://' + server + ':' + port + '/xmlrpc/object')

trans_id = datetime.now().strftime('%Y%m%d%H%M%S')

capture_picture(trans_id)

file = open(file_path +'/' + trans_id + '.jpg', "rb")  
data = file.read()  
file.close()  
byte_arr = base64.b64encode(data)

values = {}
values.update({'name': trans_id + '.jpg'})
values.update({'datas_fname': trans_id + '.jpg'})
values.update({'type': 'binary'})
values.update({'datas': byte_arr})

sock.execute(dbname, uid, pwd, 'ir.attachment', 'create', values)
