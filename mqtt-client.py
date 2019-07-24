import paho.mqtt.client as mqtt #import the client1
import time
import json
import redis
import logging
from os import path
import fcntl, socket, struct


MAC=""
TOPIC="xyz-attendance/tata"

red=redis.Redis(
    host="127.0.0.1",
    port=6379)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
print("generating log file")
basepath = path.dirname(__file__)
handler = logging.FileHandler(basepath+"mqtt-client.log","a+")
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

 

def on_connect(client, userdata, flag,rc):
    print("on_connect"+str(rc))

def on_disconnect(client, userdata, rc):
    print("in disconnect")
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")
    print("rc value in disconnect: "+str(rc))

def on_publish(client, userdata, result):
    print("in publish")
    print(result)


MAC=getHwAddr('eth0:')

# broker_address="xyzinno.tech" #use external broker
broker_address="192.168.1.137"
client = mqtt.Client(MAC) #create new instance
# client.username_pw_set("xyz-user","iot-mqtt-xyz")

client.on_connect =on_connect 		#attach function to callback
client.on_disconnect =on_disconnect
client.on_publish =on_publish 		#attach function to callback

print("connecting to broker")	
client.connect(broker_address,1883,keepalive=20) 	#connect to broker
time.sleep(1)

client.loop_start()

while True:
    
    value=red.lpop(MAC)    
    if value != None:
        print(value)
        print(value)
        ret=client.publish(TOPIC,value,qos=2)#publish
        print(ret)
        ret.wait_for_publish()
        print("data published")
    else:
        time.sleep(2)
        print("empty db")
    
