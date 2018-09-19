import json
import xmlrpclib
from xmlrpclib import Fault, Error


class Connection():

    def __init__(self, server, port, dbname, user, pwd):
        self.server = server
        self.port = port
        self.dbname = dbname
        self.user = user
        self.pwd = pwd

    def _connect(self):
        try:
            self.sock = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/common')
            self.uid = self.sock.login(self.dbname, self.user, self.pwd)
            if self.uid:
                return True, ""
            else:
                return False, ""
        except Error as err:
            return False, err.message

    def login(self):
        result, message = self._connect()
        if result:
            return True
        else:
            return False

    def get_list(self, modelname):
        result = self.login()
        if result:
            self.sock = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/object')
            args = []
            ids = self.sock.execute(self.dbname, self.uid, self.pwd, modelname, 'search', args)
            if ids:
                fields = []
                lists = self.sock.execute(self.dbname, self.uid, self.pwd, modelname, 'read', ids, fields)
                return True, lists
            else:
                return True, {}
        else:
            return False, 'Login Failed'

    def get_one(self, modelname, id):
        result = self.login()
        if result:
            self.sock = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/object')
            fields = []
            one = self.sock.execute_kw(self.dbname, self.uid, self.pwd, modelname, 'read', [id], fields)
            return True, one
        else:
            return False, 'Login Failed'

    def search(self, modelname, args, fields=[]):
        result = self.login()
        if result:
            self.sock = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/object')
            ids = self.sock.execute_kw(self.dbname, self.uid, self.pwd, modelname, 'search', args)
            if len(ids) > 0:
                lists = self.sock.execute(self.dbname, self.uid, self.pwd, modelname, 'read', ids, fields)
                return True, lists
            else:
                return True, []
        else:
            return False, 'Login Failed'

    def search_read(self, modelname, args, fields=[]):
        result = self.login()
        if result:
            self.sock = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/object')
            lists = self.sock.execute_kw(self.dbname, self.uid, self.pwd, modelname, 'search_read', args, fields)
            if len(lists) > 0:
                return True, lists
            else:
                return True, []
        else:
            return False, 'Login Failed'

    def create(self, modelname, values):
        result = self.login()
        if result:
            try:
                self.sock = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/object')
                result = self.sock.execute_kw(self.dbname, self.uid, self.pwd, modelname, 'create', values)
                if result:
                    return True, result
                else:
                    return False, 'Create Failed'
            except xmlrpclib.Fault as err:
                return False, err.faultString
        else:
            return False, 'Login Failed'

    def write(self, modelname, id, values):
        result = self.login()
        if result:
            try:
                self.sock = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/object')
                result = self.sock.execute_kw(self.dbname, self.uid, self.pwd, modelname, 'write', [[id], values])
                if result:
                    return True, {}
                else:
                    return False, 'Update Failed'
            except xmlrpclib.Fault as err:
                return False, err.faultString.search('raise')
        else:
            return False, 'Login Failed'

    def unlink(self, modelname, id, values):
        result = self.login()
        if result:
            try:
                self.sock = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/object')
                result = self.sock.execute_kw(self.dbname, self.uid, self.pwd, modelname, 'unlink', [[id]])
                if result:
                    return True, {}
                else:
                    return False, 'Delete Failed'
            except False as err:
                return False, err.message
        else:
            return False, 'Login Failed'

    def call_method(self, modelname, methodname, values):
        result = self.login()
        if result:
            try:
                self.sock = xmlrpclib.ServerProxy('http://' + self.server + ':' + self.port + '/xmlrpc/object')
                result = self.sock.execute_kw(self.dbname, self.uid, self.pwd, modelname, methodname, values)
            except Error as err:
                return False, err.message
        else:
            return False, 'Login Failed'

