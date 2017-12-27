import xmlrpclib
from xmlrpclib import Fault

try:
    username = 'operator01' #the user
    pwd = 'password'      #the password of the user
    dbname = 'park_dev_8'    #the database
    
    # Get the uid
    sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
    uid = sock_common.login(dbname, username, pwd)
    
    #replace localhost with the address of the server
    sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')
    
    args = []
        
    ids = sock.execute(dbname, uid, pwd, 'parking.pricing', 'search', args)
    
except Fault as e:
    print e
