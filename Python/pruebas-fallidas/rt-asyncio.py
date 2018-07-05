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

STOP_FLAG = False


async def streaming():
	elapsed_time = time.time()
	async for samples in sdr.stream(num_samples_or_bytes=10240000):
		audio = np.int16(fm.demodular(samples)* 32767)
		stream.write(audio)
		if STOP_FLAG:
			await sdr.stop()
	sdr.close()

stream.start_stream()

def custom_exception_handler(loop, context):
	loop.default_exception_handler(context)
	exception = context.get('exception')
	loop.stop()

loop = asyncio.get_event_loop()

# Set custom handler
loop.set_exception_handler(custom_exception_handler)
loop.run_until_complete(streaming())

while True:
	try:
		time.sleep(5)
	except KeyboardInterrupt as e:
		STOP_FLAG = True
		raise e