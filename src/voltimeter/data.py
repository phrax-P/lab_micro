import serial

ser = serial.Serial(
    port = 'COM3',\
    baudrate = 9600,\
    parity = serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0\
)

f = open('output.csv', 'w+')

print(f'connected to: {ser.portstr}')

line = []

while True:
    for c in ser.read():
        c = chr(c)
        #print(c)
        line.append(c)
        if c=='\n':
            print("Line: "+ ''.join(line))
            str = ''.join(line)
            f.write(str)
            line = []
            break
        
ser.close()