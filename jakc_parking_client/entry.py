from PyQt4.QtCore import  *
from PyQt4.QtGui import *
import json
from clientconnection import Connection


class EntryMain(QWidget):

  server = Connection('app02.jakc-labs.com', 5000)

  headers = {'Content-type': 'application/json','x-api-key': 'eiWee8ep9due4deeshoa8Peichai8Ei2'}
  data = {
    "dbname": "jewerly",
    "modelname": "account.account",
    "port": "8069",
    "pwd": "pelang1",
    "server": "app02.jakc-labs.com",
    "user": "admin"
  }

  json_foo = json.dumps(data)
  server.conn.request('POST', '/pos/api/v1.0/get_list', json_foo, headers)
  response = server.conn.getresponse()
  print(response.read().decode())


