import modbusHelper as plc
import json
import time
import paho.mqtt.client as mqtt

# Thingsboard platform credentials
THINGSBOARD_HOST = '192.168.66.98'
ACCESS_TOKEN = 'bqYfup8Bd4ejmATQjYia'

Client = None
Coils = []
Interval = 5


def on_connect(client, userdata, flags, rc, properties=None):
    """
        Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param flags: these are response flags sent by the broker
        :param rc: stands for reasonCode, which is a code for the connection result
        :param properties: can be used in MQTTv5, but is optional
    """
    client.subscribe("topic")
    print("CONNACK received with code %s." % rc)
    
def on_publish(client, userdata, mid, properties=None):
    """
        Prints mid to stdout to reassure a successful publish ( used as callback for publish )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param properties: can be used in MQTTv5, but is optional
    """
    print("mid: " + str(mid))
    
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """
        Prints a reassurance for successfully subscribing
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
        :param properties: can be used in MQTTv5, but is optional
    """
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    
def on_message(client, userdata, msg):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    data = json.loads(msg.payload)
    if data['method'] == 'motorOn':
        motorOn()
        client.publish(msg.topic.replace('request','response'),'Motor On Succeded',1)
    elif data['method'] == 'motorOff':
        motorOff()
        client.publish(msg.topic.replace('request','response'),'Motor Off Succeded',1)
        
    
next_reading = time.time()
   
Mclient = mqtt.Client("PLCDEMO")
Mclient.on_connect = on_connect
Mclient.on_subscribe = on_subscribe
Mclient.on_message = on_message
Mclient.on_publish = on_publish

Mclient.username_pw_set(ACCESS_TOKEN)
Mclient.connect(THINGSBOARD_HOST,1883,60)

if(Mclient.subscribe('v1/devices/me/rpc/request/+')):
	print("Subscribed")



Client = plc.connectModbus()

plc.writeDefaultValuesToPLC(Client,30)

while True:
	pass
#	plc.motorOn(Client)
	data = plc.readValuesFromPLC(Client)
	print(data)
	Mclient.publish('v1/devices/me/telemetry',json.dumps(data),1)
	next_reading += Interval
	sleep_time = next_reading-time.time()
	if sleep_time >0:
		time.sleep(sleep_time)
#	time.sleep(5)
#	plc.motorOff(Client)
#	data = plc.readValuesFromPLC(Client)
#	print(data)
#	Mclient.publish('v1/devices/me/telemetry',json.dumps(data))
#	time.sleep(5)
	
	
Mclient.loop_forever()

