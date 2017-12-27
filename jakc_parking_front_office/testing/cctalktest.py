import serial
import time

from ccTalk import *

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def sendMessage(header, data='', source=1, destination=2):
    request = ccTalkMessage(header=header, payload=data, source=source, destination=destination)
    request.setPayload(header, data)
    ser.write(request)
    data = ser.read(50)
    messages = parseMessages(data)
    for message in messages:
        print message
        

init = ccTalkMessage()
print init
init.setPayload(254)

ok = False

while ok!=True:
    ser.write(init)
    data = ser.read(50)
    try:
        messages = parseMessages(data)
        response = messages[-1]
        print response
    except:
        continue
    if response.payload.header == 0:
        ok = True
    else:
        print response.payload.header

sendMessage(231, '\xff\xff')

sendMessage(228, '\x01')

event = 0
while True:
    try:
        request = ccTalkMessage()
        request.setPayload(229)
        ser.write(request)
        data = ser.read(50)
        messages = parseMessages(data)
        for message in messages:
            if message.payload.header == 0:
                data = message.payload.data
                if ord(data[0]) > event:
                    event = ord(data[0])
                    print "Counter     : " + str(ord(data[0]))
                    print "Credit 1    : " + str(ord(data[1]))
                    print "Error 1     : " + str(ord(data[2]))
                    print "Credit 2    : " + str(ord(data[3]))
                    print "Error 2     : " + str(ord(data[4]))
                    print "Credit 3    : " + str(ord(data[5]))
                    print "Error 3     : " + str(ord(data[6]))
                    print "Credit 4    : " + str(ord(data[7]))
                    print "Error 4     : " + str(ord(data[8]))
                    print "Credit 5    : " + str(ord(data[9]))
                    print "Error 5     : " + str(ord(data[10]))
        time.sleep(0.2)           
    except KeyboardInterrupt, e:
        print "Quitting..."
        break
ser.close()
        