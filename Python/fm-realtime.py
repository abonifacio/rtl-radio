import asyncio
import sys
from rtlsdr import RtlSdr
from fmtools import demodular
import sounddevice as sd
import numpy as np
import pyaudio


Fs = 2.048e6
Fo = 103.7e6

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
# sdr.rs = 1024e3

sampes_queue = asyncio.Queue()
audio_queue = asyncio.Queue()

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))


# dump(sdr)

async def streaming():
	count = 0
	buff = []
	async for samples in sdr.stream():
		buff += samples
		if(count==100):
			await sampes_queue.put(buff)
			count = 0
		else:
			count +=1


    # to stop streaming:
	await sdr.stop()

    # done
	sdr.close()


async def demodulador(Fs):
	while True:
		samples = await sampes_queue.get()
		await audio_queue.put(demodular(samples,Fs))    	

async def sonido(Fs):
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paFloat32,channels=1,rate=int(Fs),output=True)
	while True:
		data = await audio_queue.get()
		stream.write(data)



loop = asyncio.get_event_loop()
loop.create_task(streaming())
loop.create_task(demodulador(Fs))
loop.create_task(sonido(48e3))
loop.run_forever()


# samples = get_muestras(1024e4)
# sFs, senial = demodular(samples,Fs)
# print(sFs)
# print(len(senial))
# sd.play(senial, sFs,blocking=True)

# async def streaming():
# 	sdr = RtlSdr()
# 	sdr.sample_rate = Fs  # Hz
# 	sdr.center_freq = Fo     # Hz
# 	sdr.freq_correction = 60   # PPM
# 	sdr.gain = 'auto'

# 	async for samples in sdr.stream():
# 		try:
# 			print(len(samples))
# 			# sFs, senial = demodular(samples,Fs)
# 			# sd.play(senial, sFs)
# 		except KeyboardInterrupt as e:
# 			break

#     # to stop streaming:
# 	await sdr.stop()

#     # done
# 	sdr.close()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(streaming())