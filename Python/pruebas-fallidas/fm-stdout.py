from multiprocessing import  Queue
from threading import  Thread
import asyncio
import sys
from rtlsdr import RtlSdr
from fmtools import demodular
import sounddevice as sd
import numpy as np
import pyaudio
import time

Fs = 2.048e6
Fo = 101.723e6

if len(sys.argv)>1:
    print(sys.argv[1])
    Fo = float(sys.argv[1]+'e6')

sdr = RtlSdr()
sdr.sample_rate = Fs  # Hz
sdr.center_freq = Fo     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt8, channels=2, rate=int(48e3), output=True)


def producer(queue):
    while True:
        queue.put(sdr.read_samples(1024e2))

def consumer(in_queue):
    while True:
        # elapsed_time = time.time()
        samples = in_queue.get()
        # print("Samples: {0}".format(time.time() - elapsed_time))
        audio = demodular(samples,Fs)
        for a in audio:
            sys.stdout.write(str(a))
            
        # elapsed_time = time.time()
        # print("Demod: {0}".format(time.time() - elapsed_time))
        # stream.write(audio)
        # out_queue.put(audio)
        # break

samples = Queue()

t_producer = Thread(target=producer,args=(samples,))
t_producer.daemon = True
t_consumer = Thread(target=consumer,args=(samples,))
t_consumer.daemon = True


t_producer.start()
t_consumer.start()

while True:
    time.sleep(2)

