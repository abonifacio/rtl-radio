import matplotlib.pyplot as plt
import numpy as np
class Plotter:

	def __init__(self,Fs,Fo):
		self.subplotDEP = 0
		self.subplotFFT = 0
		self.Fs = Fs
		self.Fo = Fo

	def clear(self):
		self.subplotDEP = 0
		self.subplotFFT = 0
		plt.figure(1)
		plt.clf()
		plt.figure(2)
		plt.clf()

	def plotBoth(self,senial,nombre):
		self.DEP(senial,nombre)
		self.FFT(senial,nombre)

	def DEP(self,senial,nombre):
		self.subplotDEP+=1
		plt.figure(1)
		plt.subplot(320 + self.subplotDEP)
		plt.title("DEP de senial "+nombre)
		plt.psd(senial, NFFT=4096, Fs=self.Fs,Fc=self.Fo,sides='twosided')

	def FFT(self,senial,nombre):
		self.subplotFFT+=1
		NFFT = len(senial)
		f = np.multiply(self.Fs/2,np.linspace(0, 1,int(NFFT/2)+1))
		Y = np.fft.fft(senial,NFFT)/NFFT
		plt.figure(2)
		plt.subplot(320 + self.subplotFFT)
		plt.title("FFT de senial "+nombre)
		plt.semilogy(f, np.multiply(2,np.abs(Y[0:int(NFFT/2)+1])))
		plt.xlabel('f [kHz]')
		plt.grid()

	def show(self):
		plt.show()