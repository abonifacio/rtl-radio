import asyncio
from multiprocessing import  Queue
from threading import  Thread
import sys
from rtlsdr import RtlSdr
from fmtools import Demodulador
import sounddevice as sd
import numpy as np
import pyaudio
import time
from scipy import signal
import matplotlib.pyplot as plt


Fs = 2.048e6
Fo = 101.723e6

if len(sys.argv)>1:
	print(sys.argv[1])
	Fo = float(sys.argv[1]+'e6')


fm = Demodulador(Fs,Fo)
output_Fs = fm.outputFs()

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,channels=1,rate=output_Fs,output=True)
sdr = RtlSdr()
sdr.sample_rate = Fs  # Hz
sdr.center_freq = Fo     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

loop = asyncio.get_event_loop()

async def streaming(queue):
	elapsed_time = time.time()
	async for samples in sdr.stream(num_samples_or_bytes=10240000):
		queue.put(samples)    
		print("Samples: {0}".format(time.time() - elapsed_time))
	# to stop streaming:
	# await sdr.stop()
	# done
	sdr.close()


def producer(queue):
	loop.run_until_complete(streaming(queue))
    

def consumer(in_queue,out_queue):
    while True:
        samples = in_queue.get()
        elapsed_time = time.time()
        audio = np.int16(fm.demodular(samples)* 32767)
        print("Demodulacion: {0}".format(time.time() - elapsed_time))
        out_queue.put(audio)
        # break

def player(queue):
    while True:
        audio = queue.get()
        elapsed_time = time.time()
        stream.write(audio)
        print("Fin copiado audio: {0}".format(time.time() - elapsed_time))
        # sd.play(audio,output_Fs)
        # break

samples = Queue()
audio = Queue()
stream.start_stream()

t_producer = Thread(target=producer,args=(samples,))
t_producer.daemon = True
t_consumer = Thread(target=consumer,args=(samples,audio,))
t_consumer.daemon = True
t_player = Thread(target=player,args=(audio,))
t_player.daemon = True

t_producer.start()
t_consumer.start()
t_player.start()

while True:
	try:
		time.sleep(5)
	except KeyboardInterrupt as e:
		sdr.stop()