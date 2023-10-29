import serial
import time
import csv

ser = serial.Serial(
    port = 'COM3',\
    baudrate = 115200,\
    parity = serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=1\
)

filename = open('data.csv','w')
output_file = csv.writer(filename)



while (1):
    data = ser.readline().decode('latin-1').replace("\n","").replace("\r","").split("\t")
    if len(data)!=4:
        continue
    print(data)
    output_file.writerow(data)
    time.sleep(1)
    
