import psycopg2

class db:

    def __init__(self, host, db, user, password):
        self.host = host
        self.dbname = db
        self.user = user
        self.password = password

    def _connectdb(self):
        self.conn = psycopg2.connect(host=self.host,database=self.dbname, user=self.user, password=self.password)

    def _closedb(self):
        self.conn.close()

    def find_transaksi_parkir(self, rfid, no_pol):
        try:
            self._connectdb()
            sql = "SELECT * FROM transaksi_parkir WHERE status=0 and no_barcode = '" + rfid + "' AND  no_pol='" + no_pol + "'"
            print sql
            cur = self.conn.cursor()
            cur.execute(sql)
            transaksi_parkir = cur.fetchone()
	    if transaksi_parkir:
  	        self._closedb()
            	return True, transaksi_parkir
	    else:
	        self._closedb()
		return False, "Transaction Parkir not Found"
        except psycopg2.DatabaseError, e:
            self._closedb()
            return False, ""

    def update_transaksi_parkir(self, rfid, no_pol, amount):
        try:
            self._connectdb()
            sql = "UPDATE transaksi_parkir SET bayar_keluar=" + str(amount) + " WHERE status=0 and no_barcode = '" + rfid + "' AND  no_pol='" + no_pol + "'"
            print sql
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            self._closedb()
            return True, ""
        except psycopg2.DatabaseError, e:
            self._closedb()
            return False, e.message

