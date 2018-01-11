import xmlrpclib
from xmlrpclib import Fault

try:
    username = 'admin' #the user
    pwd = 'P@ssw0rd'      #the password of the user
    dbname = 'parking_dev'    #the database
    
    # Get the uid
    sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
    uid = sock_common.login(dbname, username, pwd)
    
    #replace localhost with the address of the server
    sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')
    #session_data = {}
    #session_data.update({'booth_id': 1})
    #session_data.update({'operator_id': 1})
    #session_id = sock.execute(dbname, uid, pwd, 'parking.transaction.session', 'create', session_data)

    data = {}
    data.update({'plat_number':'ba1333l'})
    data.update({'booth_id':2})
    data.update({'input_method':'1'})
    data.update({'is_manless': False})
    data.update({'entry_shift_id':1})
    data.update({'entry_operator_id':1})
    
    id = sock.execute(dbname, uid, pwd, 'parking.transaction', 'create', data)
except Fault as e:
    print e


