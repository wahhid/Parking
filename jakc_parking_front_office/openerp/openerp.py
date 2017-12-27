import xmlrpclib
from xmlrpclib import Fault


class Openerp():
	
	def __init__(self, server, port, dbname , username, password):		
		self.server = server
		self.port = port
		self.dbname = dbname
		self.username = username
		self.password = password
		self.sock_common =  xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/common')
		self.sock_object = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/object')	
								
	def auth(self):
		try:
			self.uid = self.sock_common.login(self.dbname, self.username, self.password)
			return True, ""
		except Fault as e:
			return False, e


		
