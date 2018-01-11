import xmlrpclib

username = 'admin' #the user
pwd = 'P@ssw0rd'      #the password of the user
dbname = 'parking_dev'    #the database

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

values = {}
values.update({'plat_number': 'ba1333l'})
values.update({'booth_id':1})
values.update({'session_id': 1})
values.update({'input_method': '1'})
values.update({'exit_operator_id':1})
values.update({'pricing_id':1})
values.update({'state':'exit'})
result = sock.execute(dbname, uid, pwd, 'parking.transaction', 'create', values)


