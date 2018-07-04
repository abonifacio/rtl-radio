##Import Libraries 
import time
import numpy as np
import sys
import math
#import matplotlib.pyplot as plt
import sounddevice as sd
import scipy.signal as signal
from scipy.fftpack import fftshift
from scipy.io import wavfile
from rtlsdr import RtlSdr


def lpf_remez(freq,trans,Fs):
	if freq>=180e3:
		return signal.butter(4, freq / (Fs / 2), btype='low')
	else:
		return signal.butter(4, freq / (Fs / 2), btype='low')

	# return signal.remez(64, [0, freq/Fs, freq +(Fs/2-freq)/4,Fs/2], [1,0], Hz=Fs)
	# ripple_db = 60.0
	# N, beta = signal.kaiserord(ripple_db, (trans * freq)/(Fs/2))
	# print("Orden filtro ({0}) {1}".format(freq,N))
	# return signal.firwin(N, freq/(Fs/2), window=('kaiser', beta))


class Demodulador:


	def __init__(self,Fs,Fo):
		self.Fs = Fs
		self.Fo = Fo
		self.F_bw1 = 180e3
		self.F_bw2 = 15e3
		self.N1 = int(self.Fs//(self.F_bw1*2))
		self.N2 = int((self.Fs/self.N1)//(self.F_bw2*2))
		print(self.N1)
		print(self.N2)
		self.primer_filtro = lpf_remez(self.F_bw1,0.1,self.Fs)
		self.segundo_filtro = lpf_remez(self.F_bw2,0.1,(self.Fs/self.N1))
		self.output_Fs = int(self.Fs / self.N1 / self.N2)

	def lowpass(self,senial,filtro):
		return signal.lfilter(filtro[0],filtro[1], senial)

	def decimate(self,senial,N):
		# print("Long:{0},{1}".format(len(senial),N))
		return signal.decimate(senial, N)

	def discriminar(self,senial):
		D = 5
		kf = D*self.F_bw1
		y = np.unwrap(np.angle(senial))/(2*np.pi*kf)
		# y = np.concatenate(([0],np.diff(y)*self.Fs))
		y = np.diff(y)*self.Fs
		y = y - np.mean(y)
		return y

	def outputFs(self):
		return self.output_Fs 

	def demodular(self,senial):
		elapsed_time = time.time()
		# print("Pre low1: {0}".format(len(senial)))
		senial = self.lowpass(senial,self.primer_filtro)
		# print("lowpass: {0}".format(time.time() - elapsed_time))
		# print("Pre dec1: {0}".format(len(senial)))
		elapsed_time = time.time()
		senial = self.decimate(senial,self.N1)
		# print("diezmado: {0}".format(time.time() - elapsed_time))
		# print("Pre disc: {0}".format(len(senial)))
		elapsed_time = time.time()
		senial = self.discriminar(senial)
		# print("disc: {0}".format(time.time() - elapsed_time))
		elapsed_time = time.time()
		# print("Pre low2: {0}".format(len(senial)))
		senial = self.lowpass(senial,self.segundo_filtro)
		# print("lowpass2: {0}".format(time.time() - elapsed_time))
		elapsed_time = time.time()
		# print("Pre dec2: {0}".format(len(senial)))
		senial = self.decimate(senial,self.N2)
		# print("diezmado2: {0}".format(time.time() - elapsed_time))
		# print("Post dec2: {0}".format(len(senial)))
		return senial / np.max(np.abs(senial))

