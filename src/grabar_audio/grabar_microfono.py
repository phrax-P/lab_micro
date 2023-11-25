from gettext import npgettext
import serial
import time
import csv
import numpy as np
import matplotlib, wave
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
ser = serial.Serial(
    port = 'COM3',\
    baudrate = 9600,\
    #parity = serial.PARITY_NONE,\
    #stopbits=serial.STOPBITS_ONE,\
    #bytesize=serial.EIGHTBITS,\
    #timeout=1\
)

filename = open('data2.csv','w',newline="")
output_file = csv.writer(filename)

#plot_window = 20
#y_var = np.array(np.zeros([plot_window]))
#plt.ion()
#fig, ax = plt.subplots()
#line, = ax.plot(y_var)

from scipy.io.wavfile import write 
import numpy as np 
samplerate = 16000; fs = 100 
t = np.linspace(0., 1., samplerate) 
amplitude = np.iinfo(np.int16).max 
data = amplitude * np.sin(2. * np.pi * fs * t) 
write("example.wav", samplerate, data.astype(np.int16))
sound = []
print("Connection succeded")
while (1):
    try:
        data = ser.readline()
        data = int(data[0:len(data)-2].decode("utf-8").replace("\n",""))
        output_file.writerow([data])
        sound.append(data)
        #print(data)
    except:
        break
    #time.sleep(0.5)
    #y_var = np.append(y_var, float(data))
    #y_var = y_var[1:plot_window+1]
    #line.set_ydata(y_var)
    #ax.relim()
    #ax.autoscale_view()
    #fig.canvas.draw()
    #fig.canvas.flush_events()
sound = np.array(sound) # aumentar ganancia
write("example.wav", samplerate, sound.astype(np.int16))

