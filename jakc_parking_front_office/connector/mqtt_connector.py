import paho.mqtt.client as mqtt

class MQTT_Connector():
        
    def __init__(self, parent):        
        self.parent = parent        
            
    # The callback for when the client receives a CONNACK response from the server.    
    def on_connect(self, userdata, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("hello/world")
        

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, userdata, msg):
        print "Topic: ", msg.topic+'\nMessage: '+str(msg.payload)
    
    def connect(self):
        self.client = mqtt.Client()        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.parent.config.mqtt_server_ip, self.parent.config.mqtt_server_port, 60)
        self.client.loop_forever()
        
    def send(self, data):
        self.client.publish("hello/world", data)