import csv, serial
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

# Obtain data
ser = serial.Serial(
    port = '/dev/ttyACM0',\
    baudrate = 115200,\
    #parity = serial.PARITY_NONE,\
    #stopbits=serial.STOPBITS_ONE,\
    #bytesize=serial.EIGHTBITS,\
    timeout=1\
)

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
device      =   'w9fjlckvd764vq8ydotj'
client.username_pw_set(device)
client.connect(broker, port)
connected_flag = False
while not connected_flag: 
    client.loop()
    time.sleep(0.5)

filename = open('data.csv','w')
output_file = csv.writer(filename)
data_saved = {'X':[], 'Y':[], 'Z':[], 'B':[]}

print("Connection succeded")
while (1):
    data = ser.readline().decode('utf-8').replace("\n","").replace("\r","").split("\t")
    data = [int(value) for value in data]
    data['X'].append(data[0])
    data['Y'].append(data[1])
    data['Z'].append(data[2])
    #data['B'].append(row[3]) fixme kenny
    if len(data)!=3: # fixme kenny
        continue
    print(data)
    output_file.writerow(data)
    output = json.dumps(data)
    print("Topic: ", topic, "output= ", output)
    pub = client.publish(topic, output)
    client.loop()
    
client.disconnect()