import xmlrpclib
url = 'http://localhost:8069'
db = 'park_dev_8'
username = 'operator01'
password = 'password'
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
output = common.version()
print output
uid = common.login(db,username,password)
print uid