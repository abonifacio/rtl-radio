import argparse
from rtlsdr import RtlSdr
from fmtools import Demodulador
import sounddevice as sd
from temporizador import Temporizador
from plotter import Plotter

Fs = 2.048e6

parser = argparse.ArgumentParser(description='Procesar N muestras de FM.')
parser.add_argument('-n', action='store', dest='N',help='numero de muestras ej:1024e4',type=float,default=1024e4)
parser.add_argument('-f', action='store', dest='Fo',help='frecuencia centro en MHz ej:91.3',type=float,default=91.3)
parser.add_argument('--plot', action='store_true', default=False,dest='plot',help='Mostrar graficos de DEP y FFT')

args = parser.parse_args()

sdr = RtlSdr()
sdr.sample_rate = Fs  # Hz
sdr.center_freq = (args.Fo*1e6)     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

timer = Temporizador()
plotter = Plotter(Fs,(args.Fo*1e6)) if args.plot else None
fm = Demodulador(timer,plotter = plotter)

sFs = fm.outputFs()

timer.tag('inicio toma de muestras')
samples = sdr.read_samples(args.N)
timer.tag('fin toma de muestras')


audio = fm.demodular(samples)


timer.tag('reproduciendo audio')
sd.play(audio,sFs,blocking=True)
timer.tag('fin reproduccion')
timer.print()
plotter and plotter.show()