import serial
from re import search as re_search

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

reg = r'MODO\s+(?P<mode>\w+)'

f_line = True

while True:
    for c in ser.read():
        c = chr(c)
        #print(c)
        line.append(c)
        if c=='\n':
            print(''.join(line))
            str = ''.join(line)
            
            re_result = re_search(reg, str)
            if(re_result is not None):
                if(re_result.group('mode') == 'AC'):
                    if f_line:
                        f.write(str.strip())
                    else: f.write(','+ 'Vrms' + "\n" + str.strip())
                else:
                    if f_line:
                        f.write(str.strip())
                    else: f.write(',' + 'V' + "\n" + str.strip())
            else:
                f.write("," + str.strip())
                f_line = False
            line = []
            break
        
ser.close()