from jakc_parking_front_office.db.Db import db

dbconn = db('172.16.0.17','parkir_tam','postgres','P@ssw0rd')
dbconn.connectdb()
trans = dbconn.find_transaksi_parkir('7893731701','B3061UJV')
if trans:
    dbconn.update_transaksi_parkir('7893731701','B3061UJV', 21000)
dbconn.closedb()
