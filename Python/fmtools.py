import numpy as np
import scipy.signal as signal

FS = 2.048e6

def lpf_remez(freq,Fs):
	return signal.butter(4, freq / (Fs / 2), btype='low')

class Demodulador:

	def __init__(self,timer=None,plotter=None):
		self.F_bw1 = 180e3
		self.F_bw2 = 15e3
		self.N1 = int(FS//(self.F_bw1*2))
		self.N2 = int((FS/self.N1)//(self.F_bw2*2))
		self.primer_filtro = lpf_remez(self.F_bw1,FS)
		self.segundo_filtro = lpf_remez(self.F_bw2,(FS/self.N1))
		self.output_Fs = int(FS / self.N1 / self.N2)
		self.timer = timer
		self.plotter = plotter

	def lowpass(self,senial,filtro):
		return signal.lfilter(filtro[0],filtro[1], senial)

	def complex_array(self,data_array):
		data_array = np.frombuffer(data_array, dtype='uint8').astype(np.double)
		data_array = data_array - 127
		return data_array[0::2] + 1j*data_array[1::2]

	def decimate(self,senial,N):
		return signal.decimate(senial, N)

	def discriminar(self,senial): # quizás sea bueno pasar la "frecuencia de muestreo" como parámetro, por si se hace algún diezmado antes.
		D = 5
		kf = D*self.F_bw1
		y = np.unwrap(np.angle(senial))/(2*np.pi*kf)
		y = np.diff(y)*FS # creo que antes de discriminar diezmás, por lo que en vez de FS, tendrías que usar FS/N1
		y = y - np.mean(y)
		return y

	def outputFs(self):
		return self.output_Fs 

	def demodular(self,senial,toInt16 = False):
		self.plotter and self.plotter.clear()
		self.plotter and self.plotter.plotBoth(senial,'muestrada')
		
		self.timer and self.timer.tag('primer filtro')
		senial = self.lowpass(senial,self.primer_filtro)
		self.plotter and self.plotter.plotBoth(senial,'primer filtrado')
		
		self.timer and self.timer.tag('primer diezmado')
		senial = self.decimate(senial,self.N1)
		self.plotter and self.plotter.plotBoth(senial,'primer diezmado')
		
		self.timer and self.timer.tag('discriminado')
		senial = self.discriminar(senial)
		self.plotter and self.plotter.plotBoth(senial,'discriminado')

		self.timer and self.timer.tag('segundo filtro')
		senial = self.lowpass(senial,self.segundo_filtro)
		self.plotter and self.plotter.plotBoth(senial,'segundo filtro')

		self.timer and self.timer.tag('segundo diezmado')
		senial = self.decimate(senial,self.N2)
		self.plotter and self.plotter.plotBoth(senial,'segundo diezmado')

		self.timer and self.timer.tag('normalizado')
		senial = senial / np.max(np.abs(senial))

		if toInt16: return np.int16(senial* 32767)
		return senial

