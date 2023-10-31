import csv, serial
import time, json
import paho.mqtt.client as mqtt

#CLIENT METHODS
def on_connect(client, userdata, flags, rc):
    if not rc:
        client.is_connected = True
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

# Obtain data
ser = serial.Serial(
    port = '/dev/ttyACM0',\
    baudrate = 115200,\
    timeout=1\
)

#SETUP
client = mqtt.Client('B92861')
client.on_connect    = on_connect
client.on_disconnect = on_disconnect
client.on_publish    = on_publish 
client.on_log        = on_log
client.is_connected  = False
port        =   1883
broker      =   "iot.eie.ucr.ac.cr"
topic       =   "v1/devices/me/telemetry" 
username    =   'STM32 C08592/B92861'
password    =   'w9fjlckvd764vq8ydotj'
client.username_pw_set(password)
client.connect(broker, port)
while not client.is_connected: 
    client.loop()
    time.sleep(0.5)

filename = open('data.csv','w')
output_file = csv.writer(filename)
data_saved = {'X':[], 'Y':[], 'Z':[], 'B':[], 'Alert':[]}
on_off = {1: "BATERY LOW", 0: "--"}

print("Connection succeded")
while (1):
    data = ser.readline().decode('utf-8').replace("\n","").replace("\r","").split("\t")
    data = [int(value) for value in data]
    data_saved['X'].append(data[0])
    data_saved['Y'].append(data[1])
    data_saved['Z'].append(data[2])
    data_saved['B'].append(data[3])
    data_saved['Alert'].append(data[4])
    if len(data)!=5:
        continue
    output_file.writerow(data)
    output = json.dumps({"X": data[0], "Y": data[1], "Z": data[2], "B": data[3], "Alert":on_off[data[4]]})
    print("Topic: ", topic, "output= ", output)
    pub = client.publish(topic, output)
    client.loop()
    