import httplib, urllib


class Connection:

    def __init__(self, url, port=80):
        self.url = url
        self.port = port
        self.connect()

    def connect(self):
        self.conn = httplib.HTTPConnection(self.url + ":" + str(self.port))
