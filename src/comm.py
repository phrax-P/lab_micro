# python3.6

import random
import serial
from paho.mqtt import client as mqtt_client
from re import search as re_search


broker = 'broker.emqx.io'
port = 1883
topic = "carrito"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
command = ''
# username = 'emqx'
# password = 'public'

# Obtain data
ser = serial.Serial(
port = 'COM9',\
baudrate = 9600,\
timeout=1\
)


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received {msg.payload.decode()} from {msg.topic} topic")
        command = msg.payload.decode()
        reg = r'messages:\s+(?P<comando>\w+)'
        reg_result = re_search(reg,command).group('comando')
        if(reg_result == 'ARRIBA'):
            ser.write(b'F')
        elif(reg_result == 'ABAJO'):
            ser.write(b'B')
        elif(reg_result == 'IZQUIERDA'):
            ser.write(b'L')
        elif(reg_result == 'DERECHA'):
            ser.write(b'R')
        elif(reg_result == 'STOP'):
            ser.write(b'S')


    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()