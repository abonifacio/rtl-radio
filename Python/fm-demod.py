##Import Libraries 
import numpy as np
import sys
import matplotlib.pyplot as plt
import sounddevice as sd
import scipy.signal as signal
from scipy.fftpack import fftshift
from scipy.io import wavfile
from rtlsdr import RtlSdr

plot = False
plot = True

class Plotter:

	def __init__(self,Fs,Fo):
		self.subplotDEP = 0
		self.subplotFFT = 0
		self.Fs = Fs
		self.Fo = Fo

	def plot(self,senial,nombre,fft = True):
		# return
		# self.DEP(senial,nombre)
		if fft:
			self.FFT(senial,nombre)
		else: 
			self.subplotFFT+=1

	def DEP(self,senial,nombre):
		self.subplotDEP+=1
		plt.figure(1)
		plt.subplot(320 + self.subplotDEP)
		plt.title("DEP de senial "+nombre)
		plt.psd(senial, NFFT=4096, Fs=self.Fs,Fc=self.Fo,sides='twosided')

	def FFTOLD(self,senial,nombre):
		self.subplotFFT+=1
		plt.figure(2)
		plt.subplot(220 + self.subplotFFT)
		plt.title("FFT de senial "+nombre)
		n = len(senial) # length of the signal
		k = np.arange(n)
		T = n/self.Fs
		frq = k/T # two sides frequency range
		frq = frq[range(int(n/2))] # one side frequency range
		# n = np.arange(-50,51)
		N = 1024
		Ts = 1/self.Fs
		Y = np.fft.fft(senial)/n # fft computing and normalization
		Y = Y[range(int(n/2))]
		# Y = np.fft.fftshift(np.fft.fft(senial))
#		f = [(1-(1/N)*mod(N,2))*(-1/(2*Ts)):(1/N)*(1/Ts):((N-1)/N) * (1/(2*Ts))]
		# f = np.arange((1-(1/N)*np.mod(N,2))*(-1/(2*Ts)),((N-1)/N) * (1/(2*Ts)),(1/N)*(1/Ts))
		plt.plot(frq,Y)

	def FFT(self,senial,nombre):
		self.subplotFFT+=1
		NFFT = len(senial)
		f = np.multiply(self.Fs/2,np.linspace(0, 1,int(NFFT/2)+1))
		Y = np.fft.fft(senial,NFFT)/NFFT
		plt.figure(2)
		plt.subplot(320 + self.subplotFFT)
		plt.title("FFT de senial "+nombre)
		# f, Pxx = signal.welch(senial, self.Fs, detrend=lambda x: x)
		# f, Pxx = fftshift(f), fftshift(Pxx)
		plt.semilogy(f, np.multiply(2,np.abs(Y[0:int(NFFT/2)+1])))
		plt.xlabel('f [kHz]')
		plt.ylabel('PSD [Power/Hz]')
		plt.grid()
		# plt.xticks(np.linspace(-self.Fs/2e3, self.Fs/2e3, 7))
		# plt.xlim(-self.Fs/2e3, self.Fs/2e3)

	def show(self):
		plt.show()


def get_muestras(n_samples,sample_rate,center_freq):
	sdr = RtlSdr()
	sdr.sample_rate = sample_rate
	sdr.center_freq = center_freq
	sdr.freq_correction = 60
	sdr.gain = 20
	return sdr.read_samples(n_samples)

def get_muestras_fixed():
	data_array = np.fromfile("C:/Users/Augusto/Downloads/Laboratorio/Matlab/Samples",dtype="uint8").astype(np.double)
	data_array = data_array - 127
	print(np.mean(data_array))
	return data_array[0::2] + 1j*data_array[1::2]

def low_pass(senial,freq):
	lpf = signal.remez(64, [0, freq, freq +(Fs/2-freq)/4,Fs/2], [1,0], Hz=Fs)
	# lpf = signal.remez(64, [0, freq, freq +(Fs/2-freq)/2,Fs/2], [1,0], Hz=Fs)
	return signal.lfilter(lpf, 1.0, senial)

def decimate(senial,N):
	return signal.decimate(senial, N)

def discriminar(senial):
	global Fs
	W = 180e3
	D = 15
	kf = D*W
	print('np.unwrap(np.angle(np.hilbert(senial)))')
	y = signal.hilbert(np.real(senial))
	print('np.unwrap(np.angle(y))')
	y = np.unwrap(np.angle(y))
	print('y/(2*np.pi*kf)')
	y = y/(2*np.pi*kf)
	print('[0, np.diff(y)*Fs]')
	# y = [0, np.diff(y)*Fs]
	y = np.concatenate(([0],np.diff(y)*Fs));
	print('y-np.mean(y)')
	y = np.subtract(y,np.mean(y)) 
	return np.divide(y,np.max(np.abs(y)))
	# return np.diff(y)
	# y = senial[1:] * np.conj(senial[:-1])
	# return np.angle(y) 

def discriminar2(senial):
	# return np.diff(y)
	y = senial[1::1] * np.conjugate(senial[0:-1:1])
	return np.angle(y) 

# xd = unwrap(angle(hilbert(data)));
# xd = xd/(2*pi*kf); 
# yd = xd-mean(xd); 
# yd =  yd/max(abs(yd));


## Import data from file 
N_MUESTRAS = 1024e4
Fo = 101.723e6
Fs = 2.048e6
F_bw1 = 180e3
F_bw2 = 48e3

plotter = Plotter(Fs,Fo)

if len(sys.argv)>1:
	print(sys.argv[1])
	Fo = float(sys.argv[1]+'e6')


senial = get_muestras(N_MUESTRAS,Fs,Fo)
# senial = get_muestras_fixed()
plotter.plot(senial,"muestreada")

senial = low_pass(senial,F_bw1)
plotter.plot(senial,"filtrada (180k)")

Fs = Fs / 10	
senial = decimate(senial,10)
plotter.plot(senial,"diezmada (1)")

senial = discriminar(senial)
plotter.plot(senial,"discriminada")

senial = low_pass(senial,F_bw2)
plotter.plot(senial,"filtrada (48k)")

Fs = Fs / 4

senial = decimate(senial,4)
plotter.plot(senial,"diezmada (2)")

# plotter.show()

senial = senial / np.max(np.abs(senial)) 

# senial = np.int16(senial/np.max(np.abs(senial)) * 3276700)
# senial = np.int16(senial)

print(len(senial))
print(Fs)

# senial.astype("int16").tofile("C:/Users/Augusto/Downloads/Samples-out.raw")
# wavfile.write("comercial_demodulated.wav", rate=int(Fs), data=senial)

sd.play(senial, Fs, blocking=True)
