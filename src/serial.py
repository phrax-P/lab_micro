import serial

# Obtain data
ser = serial.Serial(
    port = 'COM9',\
    baudrate = 115200,\
    timeout=1\
)

while (1):
    data_receive = ser.readline()
    print(data_receive)
    ser.write(b'f')