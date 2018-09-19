from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, redirect, url_for, request, session, Response
from flask_login import login_required, current_user
import serial, time, threading
from Queue import Queue
import json
import sys
import glob
from flask_socketio import SocketIO, emit, join_room, leave_room
from jakc_parking_client.odooapi.connection import Connection


serverName = 'app02.jakc-labs.com'
serverPort = '8069'
dbName = 'parking'
ser = None


#def getSerialData():
#    while True:
#        if serialExist:
#            stuff = str(ser.readline().decode('utf-8'))
#            get_serial_data(stuff)
#            time.sleep(1)
#        else:
#            time.sleep(1)
#            print "No Serial Device Found"




app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)


def getSerialData():
    ser = None
    #rts = False

    def flag_rts():
        rts = True

    while True:
        try:
            if (ser == None):
                ser = serial.Serial('/dev/cu.usbmodem1421', baudrate=9600, timeout=10)
            stuff = str(ser.readline().decode('utf-8'))
            time.sleep(0.1)
            get_serial_data(stuff)
        except:
            if (not (ser == None)):
                ser.close()
                ser = None
                print("Disconnecting")

            print("No Connection")
            time.sleep(2)


def get_serial_data(data):
    print "get serial data"
    print data
    if data.strip() == 'RT':
        print "Detect Request Ticket"
        socketio.emit('parking device', {'data': 'RT'}, namespace='/test')
    if data.strip() == 'CD':
        print "Card Detected"
        socketio.emit('parking device', {'data': 'CD'}, namespace='/test')

q = Queue()
serialThread  = threading.Thread(name='serialThread', target=getSerialData)
serialThread.start()


@app.route('/')
def index():
    return render_template("login1.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        booth = request.form['booth']
        conn = Connection(serverName, serverPort, dbName, username, password)
        res = conn.login()
        if res:
            status, userprofile = conn.get_one('res.users', conn.uid)
            user = {'username':username, 'password':password}
            status = {'status': True, 'message':'Login Successfully'}
            session['username'] = username
            session['password'] = password
            session['profile'] = userprofile[0]
            #Find Booth
            booth_args = [[['code','=', booth]]]
            status, booth_ids = conn.search('parking.booth', booth_args)
            if status:
                booth_id = booth_ids[0]
                session['booth_id'] = booth_id.get('id')
                session['booth_code'] = booth_id.get('code')
                session['booth_name'] = booth_id.get('name')
                session['booth_type'] = booth_id.get('booth_type')
                if booth_id.get('booth_type') == 'out' or booth_id.get('booth_type') == 'inout':
                    session_values = {}
                    session_values.update({'booth_id': booth_id.get('id')})
                    session_values.update({'operator_id': conn.uid})
                    session_list = []
                    session_list.append(session_values)
                    res, trans_session = conn.create('parking.transaction.session', session_list)
                    if not status:
                        print "Error Session"
                        print trans_session
                        status = {'status': False, 'message': trans_session}
                        return redirect(url_for('index'))
                    session['session_id'] = trans_session
            else:
                status = {'status': False, 'message': 'Booth not Found'}
                return redirect(url_for('index'))

            #Redirect to Screen
            if booth_id.get('booth_type') == 'in':
                if booth_id.get('is_manless'):
                    return redirect(url_for('screen_manless'))
                else:
                    return redirect(url_for('screen_client'))
            else:
                return redirect(url_for('screen_client'))
        else:
            status = {'status': False, 'message': 'Username or Password was wrong'}
            return redirect(url_for('index'))
    else:
        status = {'status': False, 'message': 'Username or Password was wrong'}
        return  redirect(url_for('index'))

@app.route('/client')
def screen_client():
    return render_template("client1.html")

@app.route('/manless')
def screen_manless():
    return render_template("manless1.html")


@app.route('/parking/transaction/create', methods=['POST','GET'])
def parking_transaction_create():
    if request.method == 'POST':
        print "Create Transaction"
        if 'platnumber' in request.form.keys():
            platnumber = request.form['platnumber']
        if 'barcode' in request.form.keys():
            barcode = request.form['barcode']

        input_method = request.form['input_method']
        image01 = request.form['image01']
        if session['booth_type'] == 'in':
            conn = Connection('app02.jakc-labs.com', '8069', 'parking', session['username'], session['password'])
            res = conn.login()
            if res:
                parking_values = {}
                print "Login Successfully"
                parking_values = {}
                parking_values.update({'input_method': input_method})
                parking_values.update({'booth_id': session['booth_id']})
                parking_values.update({'entry_operator_id': conn.uid})
                if 'platnumber' in request.form.keys():
                    parking_values.update({'plat_number': platnumber})
                if 'barcode' in request.form.keys():
                    if len(barcode) > 0:
                        parking_values.update({'barcode': barcode})
                parking_values.update({'entry_front_image': image01.split(',')[1]})
                parking_list = []
                parking_list.append(parking_values)
                print parking_list
                res, message = conn.create('parking.transaction', parking_list)
                if res:
                    datas = []
                    status = {'status': res, 'message': message}
                    datas.append(status)
                    return Response(json.dumps(datas), mimetype='application/json')
                else:
                    datas = []
                    status = {'status': res, 'message': message}
                    datas.append(status)
                    return Response(json.dumps(datas), mimetype='application/json')

            else:
                datas = []
                status = {'status': False, 'message': 'Session Problem'}
                datas.append(status)
                return Response(json.dumps(datas), mimetype='application/json')
        if session['booth_type'] == 'out':
            print "out"
            barcode = request.form['barcode']
            parking_values = {}
            conn = Connection(serverName, serverPort, dbName, session['username'], session['password'])
            res = conn.login()
            if res:
                parking_values.update({'session_id': session['session_id']})
                parking_values.update({'input_method': input_method})
                parking_values.update({'booth_id': session['booth_id']})
                parking_values.update({'exit_operator_id': conn.uid})
                parking_values.update({'barcode': barcode})
                parking_values.update({'plat_number': platnumber})
                parking_values.update({'exit_front_image': image01.split(',')[1]})
                parking_values.update({'pricing_id': 1})
                parking_list = []
                parking_list.append(parking_values)
                res, message = conn.create('parking.transaction', parking_list)
                if res:
                    datas = []
                    res, message = conn.get_one('parking.transaction', message)
                    status = {'status': res, 'message': message}
                    datas.append(status)
                    print status
                    return Response(json.dumps(datas), mimetype='application/json')
                else:
                    datas = []
                    status = {'status': res, 'message': message}
                    datas.append(status)
                    print status
                    return Response(json.dumps(datas), mimetype='application/json')
            else:

                datas = []
                status = {'status': False, 'message': 'Session Problem'}
                datas.append(status)
                print status
                return Response(json.dumps(datas), mimetype='application/json')
    else:
        datas = []
        status = {'status': False, 'message': 'Method not accepted'}
        datas.append(status)
        print status
        return Response(json.dumps(datas), mimetype='application/json')


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})
    emit('my response', {'data': 'REA:0001:0001'}, )


@socketio.on('my event', namespace='/test')
def test_message(message):
    print "Receive Data : " + message['data']
    #emit('my response', {'data': message['data']})
    #getSerialData().flag_rts()


@socketio.on('parking machine', namespace='/test')
def parking_machine(message):
    print "Receive Data : " + message['data']
    #getSerialData().flag_rts()


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

#@socketio.on('disconnect', namespace='/test')
#def test_disconnect():
#    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)