import socket
from multiprocessing import  Queue
from threading import  Thread
import asyncio
import sys
# from rtlsdr import RtlSdr
# import soundcard as sc
from fmtools import Demodulador
import sounddevice as sd
import numpy as np
import pyaudio
import time
import pytcp
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
stream = p.open(format=pyaudio.paInt16,channels=1,rate=output_Fs,output=True)
# default_speaker = sc.default_speaker()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))


def producer(queue):
    pytcp.init(samples_queue)
    # while True:
    #     elapsed_time = time.time()
    #     # samples = sdr.read_samples(1024e4)
    #     samples = complex_array(s.recv(BUFFER_SIZE))
    #     # print("Muestras por segundo {0}".format(len(samples)/(time.time()-elapsed_time)))
    #     # for spl_array in np.split(samples,10):
    #     #     queue.put(spl_array)
    #     queue.put(samples)
    #     # print("Samples: {0}".format(time.time() - elapsed_time))
        # break

def consumer(in_queue,out_queue):
    elapsed_time = time.time()
    while True:
        samples = in_queue.get()
        # print("Samples: {0}".format(time.time() - elapsed_time))
        # elapsed_time = time.time()
        audio = np.int16(fm.demodular(samples)* 32767)
        # audio = fm.demodular(samples)

        # audio = fm.demodular(samples)
        # print("Demodulacion: {0}".format(time.time() - elapsed_time))
        # print("Demod: {0}".format(time.time() - elapsed_time))
        # time.sleep(1)
        print("Muestras: {0} ===== Segundos de audio: {1} cada: {2} ({3})".format(len(audio),len(audio)/output_Fs,time.time()-elapsed_time,output_Fs))
        elapsed_time = time.time()
        out_queue.put(audio)
        # break

def player(queue):
    count = 0
    buffer = []
    while True:
        audio = queue.get()
        stream.write(audio)
        # default_speaker.play(audio, samplerate=output_Fs)
        # while(len(buffer)<4096*1024):
        #     buffer += audio
        # print(len(buffer))
        # buffer = []
        # sd.play(audio,output_Fs,blocking=False)


samples_queue = Queue()
audio = Queue()
stream.start_stream()

t_producer = Thread(target=producer,args=(samples_queue,))
t_producer.daemon = True
t_consumer = Thread(target=consumer,args=(samples_queue,audio,))
t_consumer.daemon = True
t_consumer2 = Thread(target=consumer,args=(samples_queue,audio,))
t_consumer2.daemon = True
t_consumer3 = Thread(target=consumer,args=(samples_queue,audio,))
t_consumer3.daemon = True
t_player = Thread(target=player,args=(audio,))
t_player.daemon = True

t_producer.start()
t_consumer.start()
# t_consumer2.start()
# t_consumer3.start()
t_player.start()

while True:
    time.sleep(5)
    # try:
    # except KeyboardInterrupt as e:
    #     s.close()
    #     raise e

# b, a = signal.butter(34, 180e3, 'low', analog=True)
# w, h = signal.freqs(b, a)
# plt.plot(w, 20 * np.log10(abs(h)))
# plt.xscale('log')
# plt.title('Butterworth filter frequency response')
# plt.xlabel('Frequency [radians / second]')
# plt.ylabel('Amplitude [dB]')
# plt.margins(0, 0.1)
# plt.grid(which='both', axis='both')
# plt.axvline(100, color='green') # cutoff frequency
# plt.show()
