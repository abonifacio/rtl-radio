import socket
from multiprocessing import  Queue
from threading import  Thread
import asyncio
import sys
# from rtlsdr import RtlSdr
from fmtools import Demodulador
import sounddevice as sd
import numpy as np
import pyaudio
import time
import pytcp2
import pyudp
from scipy import signal
#import matplotlib.pyplot as plt

TCP_IP = '127.0.0.1'
TCP_PORT = 1234
BUFFER_SIZE = 128*2**20


Fs = 2.048e6
# Fs = 3.2e6
Fo = 101.723e6

if len(sys.argv)>1:
    print(sys.argv[1])
    Fo = float(sys.argv[1]+'e6')

# sdr = RtlSdr()
# sdr.sample_rate = Fs  # Hz
# sdr.center_freq = Fo     # Hz
# sdr.freq_correction = 60   # PPM
# sdr.gain = 'auto'

fm = Demodulador(Fs,Fo)

output_Fs = fm.outputFs() 
print(output_Fs)
 # 0.0005371146202599635
 # 0.0005371146202599635

def callback(in_data, frame_count, time_info, status):
    data = audio.get()
    return (data, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt8,channels=1,rate=output_Fs,output=True)


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))

def callback(data):
	tmp = time.time()
	# audio = fm.demodular(data).astype(np.int8)
	audio = np.int32(fm.demodular(data)* 32767)
	# pyudp.send(audio)
	stream.write(audio)
	# print("Tiempo demod: {0} Segundos de audio: {1}".format(time.time()-tmp,len(audio)/output_Fs))
	# sd.play(fm.demodular(data),output_Fs,blocking=False)

pytcp2.init(callback)

while True:
    time.sleep(5)
    # try:
    # except KeyboardInterrupt as e:
    #     s.close()
    #     raise e
