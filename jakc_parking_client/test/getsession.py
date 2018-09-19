from jakc_parking_client.odooapi.connection import Connection
#import cv2

if __name__ == '__main__':
    conn = Connection('app02.jakc-labs.com','8069','parking', 'admin','pelang1')
    res = conn.login()
    uid = conn.uid
    if res:
        print "Login Successfully"
    filters = [['booth_id','=',2],['operator_id','=', uid]]

    #Create Session
    session_values = {}
    session_values.update({'booth_id': 2})
    session_values.update({'operator_id': uid})
    session_list = []
    session_list.append(session_values)
    res, message = conn.create('parking.transaction.session', session_list)
    print res
    print message
