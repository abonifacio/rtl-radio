from multiprocessing import  Queue
from fmtools import Demodulador
from threading import  Thread
import pyaudio
import tcpclient
from temporizador import Temporizador


def producer(in_queue,out_queue):
    while True:
        byte_array = in_queue.get()
        out_queue.put(fm.complex_array(byte_array)) 

def consumer(in_queue,out_queue):
    while True:
        samples = in_queue.get()
        audio = fm.demodular(samples,toInt16=True)
        stream.write(audio)

fm = Demodulador()
output_Fs = fm.outputFs() 

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,channels=1,rate=output_Fs,output=True)

samples_queue = Queue()
iq_queue = Queue()
audio_queue = Queue()
stream.start_stream()

t_producer = Thread(target=producer,args=(samples_queue,iq_queue,))
t_producer.daemon = True
t_consumer = Thread(target=consumer,args=(iq_queue,audio_queue,))
t_consumer.daemon = True

t_producer.start()
t_consumer.start()


tcpclient.init(samples_queue)
