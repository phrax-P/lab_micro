import serial, json, time
import paho.mqtt.client as mqtt

# parameters
port        =   1883
broker      =   "iot.eie.ucr.ac.cr"
topic       =   "v1/devices/me/telemetry" 
username    =   'C08592/B92861'
password    =   'brjxmov6h994bpdea2fr'

#CLIENT METHODS
def on_connect(client, userdata, flags, rc):
    if not rc:
        client.is_connected = True
        client.subscribe(topic)
        print('Connection established. Working')
    else:
        print('Connection Faild', rc)
        client.loop_stop()

def on_disconnect(client, userdata, rc):
    if(rc == 0):
        print("Client disconneted OK")
    else:
        print("System disconnected via code: ", rc)

def on_log(client, userdata, level, buf):
   print(buf) 

def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)

def on_message(client, userdata, message):
    message_received=str(message.payload.decode("utf-8"))
    msg = json.loads(message_received)
    print(msg)
    
#SETUP
client = mqtt.Client('B92861')
client.on_connect    = on_connect
client.on_disconnect = on_disconnect
client.on_publish    = on_publish 
client.on_log        = on_log
client.on_message = on_message
client.is_connected  = False
client.username_pw_set(password)
client.connect(broker, port)
while not client.is_connected: 
    client.loop()
    time.sleep(0.5)
    
# Obtain data
#ser = serial.Serial(
#    port = 'COM9',\
#    baudrate = 115200,\
#    timeout=1\
#)

while (1):
    #data_receive = ser.readline()
    #print(data_receive)
    client.loop()
    #ser.write(b'f')