import sys
from rtlsdr import RtlSdr
from fmtools import Demodulador
import sounddevice as sd
from scipy import signal
import numpy as np

Fs = 2.048e6
Fo = 92.1e6

if len(sys.argv)>1:
    print(sys.argv[1])
    Fo = float(sys.argv[1]+'e6')

def get_muestras_fixed():
    data_array = np.fromfile("C:/Users/Augusto/Downloads/Laboratorio/Matlab/Muestras-91.1",dtype="uint8").astype(np.double)
    data_array = data_array - 127
    return data_array[0::2] + 1j*data_array[1::2]

sdr = RtlSdr()
sdr.sample_rate = Fs  # Hz
sdr.center_freq = Fo     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

samples = sdr.read_samples(1024e4)

fm = Demodulador(Fs,Fo)
sFs = fm.outputFs()
# samples = get_muestras_fixed()

audio = fm.demodular(samples)
sd.play(audio,sFs,blocking=True)
