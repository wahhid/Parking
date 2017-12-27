import xmlrpclib
from xmlrpclib import Fault

try:
    username = 'admin' #the user
    pwd = 'P@ssw0rd'      #the password of the user
    dbname = 'park_dev_7'    #the database
    
    # Get the uid
    sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
    uid = sock_common.login(dbname, username, pwd)
    
    #replace localhost with the address of the server
    sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

    fields = []
    shift = sock.execute(dbname, uid, pwd, 'parking.shift', 'read', [1], fields)
    print shift
    
except Fault as e:
    print e