import argparse,time
from multiprocessing import  Queue
from threading import  Thread
from fmtools import Demodulador
import numpy as np
import pyaudio
import tcpclient
from temporizador import Temporizador


parser = argparse.ArgumentParser(description='Intento de FM en tiempo real.')
parser.add_argument('-s', action='store', default=0,type=int,dest='seconds',help='Correr por s segundos con toma de tiempos')

args = parser.parse_args()



fm = Demodulador()
output_Fs = fm.outputFs() 
timer = Temporizador(args.seconds!=0)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,channels=1,rate=output_Fs,output=True)


def producer(queue):
    tcpclient.init(queue)

def consumer(in_queue,out_queue):
    while True:
        samples = in_queue.get()
        timer.tag('inicio consumer')
        audio = fm.demodular(samples,toInt16=True)
        out_queue.put(audio)
        timer.tag('fin consumer')

def player(queue):
    while True:
        audio = queue.get()
        timer.tag('recibido audio')
        stream.write(audio)
        timer.tag('muestras copiadas al buffer de audio')

samples_queue = Queue()
audio = Queue()
stream.start_stream()

t_producer = Thread(target=producer,args=(samples_queue,))
t_producer.daemon = True
t_consumer = Thread(target=consumer,args=(samples_queue,audio,))
t_consumer.daemon = True
t_consumer2 = Thread(target=consumer,args=(samples_queue,audio,))
t_consumer2.daemon = True
t_consumer3 = Thread(target=consumer,args=(samples_queue,audio,))
t_consumer3.daemon = True
t_player = Thread(target=player,args=(audio,))
t_player.daemon = True

t_producer.start()
t_consumer.start()
t_consumer2.start()
t_consumer3.start()
t_player.start()

if args.seconds:
    time.sleep(args.seconds)
    timer.print()
else:
    while True:
        time.sleep(5)
