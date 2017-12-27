import xmlrpclib

username = 'admin' #the user
pwd = 'P@ssw0rd'      #the password of the user
dbname = 'park_dev_7'    #the database

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

args = [('plat_number','=','012015071408393547215'),('state','=','entry')] #query clause
ids = sock.execute(dbname, uid, pwd, 'parking.transaction', 'search', args)
if ids:
    values = {}
    values.update({'exit_booth_id':1})
    values.update({'exit_shift_id':1})
    values.update({'exit_operator_id':1})
    values.update({'pricing_id':1})
    values.update({'state':'exit'})     
    result = sock.execute(dbname, uid, pwd, 'parking.transaction', 'write', ids, values)
else:
    print('Car Not Exist')


