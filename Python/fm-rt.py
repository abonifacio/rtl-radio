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


def get_muestras(n_samples):
	sdr = RtlSdr()
	sdr.sample_rate = Fs
	sdr.center_freq = Fo
	sdr.freq_correction = 60
	sdr.gain = 'auto'
	return sdr.read_samples(n_samples)

sdr = RtlSdr()
sdr.sample_rate = Fs  # Hz
sdr.center_freq = Fo     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'



p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,channels=1,rate=int(15e3),output=True)

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))


# dump(sdr)

def on_samples(samples,object):
	elapsed_time = time.time()
	audio = demodular(samples,Fs)
	print("Demod total: {0}".format(time.time() - elapsed_time))
	# elapsed_time = time.time()
	# stream.write(audio)
	sd.play(audio,int(48e3),blocking=True)
	# print("Longitud audio: {0}".format(len(audio)))
	# print("Sonido 2: {0}".format(time.time() - elapsed_time))
	
while(True):
	elapsed_time = time.time()
	samples = sdr.read_samples(1024e4)
	print("Muestras leidas en: {0}".format(time.time() - elapsed_time))
	on_samples(samples,False)


# dump(filtro_15k)
# dump(filtro_180k)

# sdr.read_samples_async(on_samples, num_samples=1024e4)
