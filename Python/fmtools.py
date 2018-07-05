import numpy as np
import scipy.signal as signal
from temporizador import Temporizador

FS = 2.048e6

def lpf_remez(freq,trans,Fs):
	return signal.butter(4, freq / (Fs / 2), btype='low')

class Demodulador:

	def __init__(self,timer=Temporizador(False)):
		self.F_bw1 = 180e3
		self.F_bw2 = 15e3
		self.N1 = int(FS//(self.F_bw1*2))
		self.N2 = int((FS/self.N1)//(self.F_bw2*2))
		self.primer_filtro = lpf_remez(self.F_bw1,0.1,FS)
		self.segundo_filtro = lpf_remez(self.F_bw2,0.1,(FS/self.N1))
		self.output_Fs = int(FS / self.N1 / self.N2)
		self.timer = timer

	def lowpass(self,senial,filtro):
		return signal.lfilter(filtro[0],filtro[1], senial)

	def decimate(self,senial,N):
		return signal.decimate(senial, N)

	def discriminar(self,senial):
		D = 5
		kf = D*self.F_bw1
		y = np.unwrap(np.angle(senial))/(2*np.pi*kf)
		y = np.diff(y)*FS
		y = y - np.mean(y)
		return y

	def outputFs(self):
		return self.output_Fs 

	def demodular(self,senial,toInt16 = False):
		self.timer.tag('primer filtro')
		senial = self.lowpass(senial,self.primer_filtro)
		self.timer.tag('primer diezmado')
		senial = self.decimate(senial,self.N1)
		self.timer.tag('discriminado')
		senial = self.discriminar(senial)
		self.timer.tag('segundo filtro')
		senial = self.lowpass(senial,self.segundo_filtro)
		self.timer.tag('segundo diezmado')
		senial = self.decimate(senial,self.N2)
		self.timer.tag('normalizado')
		senial = senial / np.max(np.abs(senial))
		if toInt16:
			return np.int16(senial* 32767)
		return senial

