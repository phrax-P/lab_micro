import csv
import time, json
import paho.mqtt.client as mqtt


#CLIENT METHODS
def on_connect(client, userdata, flags, rc):
    if rc:
        connected_flag = True
        print('Connection established. Working')
    else:
        print('Connection Faild', rc)
        client.loop_stop()

def on_disconnect(client, userdata, rc):
    print("Disconnection successful")

def on_log(client, userdata, level, buf):
   print(buf) 

def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)

#SETUP
mqtt.Client.connect_flag        = False
mqtt.Client.suppress_exceptions = False
client = mqtt.Client('py1')
client.on_connect    = on_connect
client.on_disconnect = on_disconnect
client.on_publish    = on_publish 
client.on_log        = on_log
port        =   1883
broker      =   "iot.eie.ucr.ac.cr"
topic       =   "v1/devices/me/telemetry" 
username    =   'STM32 C08592/B92861'
password    =   'w9fjlckvd764vq8ydotj'
client.username_pw_set(username, password)
client.connect(broker, port)
connected_flag = False
while not connected_flag: 
    client.loop()
    time.sleep(0.5)


data = {'X':[], 'Y':[], 'Z':[], 'B':[]}

#SEND INFORMATION
with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        data['X'].append(row[0])
        data['Y'].append(row[1])
        data['Z'].append(row[2])
        data['B'].append(row[3])
        output = json.dumps(data)
        print("Topic: ", topic, "output= ", output)
        pub = client.publish(topic, output, 0)
        time.sleep(1)
        
client.disconnect()