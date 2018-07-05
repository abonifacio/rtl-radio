import time
from fmtools import Demodulador
from rtlsdr.rtlsdrtcp.client import RtlSdrTcpClient
import sounddevice as sd
import numpy as np
import pyaudio

Fs = 2.048e6
Fo = 91.3e6
client = RtlSdrTcpClient(hostname='127.0.0.1', port=12345)
client.center_freq = Fo 

fm = Demodulador(Fs,Fo)
sFs = fm.outputFs()

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,channels=1,rate=sFs,output=True)

stream.start_stream()

while True:
	data = client.read_samples()
	audio = fm.demodular(data)
	if(len(audio)>27):
		audio = np.int16(fm.demodular(audio)* 32767)
		stream.write(audio)
	else:
		print(len(audio))
	# sd.play(audio,sFs,blocking=True)
	time.sleep(0.2)
