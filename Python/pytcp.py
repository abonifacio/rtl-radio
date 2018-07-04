import asyncore
import socket, time
import numpy as np
import struct

# reference time (in seconds since 1900-01-01 00:00:00)
# TIME1970 = 2208988800L # 1970-01-01 00:00:00


class TCPClient(asyncore.dispatcher):
    # time requestor (as defined in RFC 868)

    BUFF_SIZE = 8192*1024
    # BUFF_SIZE = 8192

    def __init__(self, queue):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(('127.0.0.1', 1234))
        self.queue = queue
        self.buffer = bytearray()
        self.time = time.time()

    def complex_array(self,data_array):
        data_array = np.frombuffer(data_array, dtype='uint8').astype(np.double)
        data_array = data_array - 127
        return data_array[0::2] + 1j*data_array[1::2]

    def writable(self):
        return 0 # don't have anything to write

    def handle_connect(self):
        pass # connection succeeded

    def handle_expt(self):
        self.close() # connection failed, shutdown

    def handle_read(self):
        s = self.recv(self.BUFF_SIZE)
        len_s = len(s)
        if len_s>15:
        	for i in range(0,len_s):
        		self.buffer.append(s[i])
	        	# self.buffer.append(1j*(struct.unpack("B", s[i+1])-127))
        	if len(self.buffer)>=self.BUFF_SIZE:
        		# print("Muestras {0}".format(len(self.buffer)))
        		self.queue.put(self.complex_array(self.buffer))
        		self.buffer = bytearray()
        		# print("Tiempo de muestras: {0}".format(time.time()-self.time))
        		self.time = time.time()
    # def handle_read(self):
    #     s = self.recv(self.BUFF_SIZE)
    #     if len(s)>15:
    #     	self.queue.put(self.complex_array(s))

    def handle_close(self):
        self.close()


def init(queue):
	request = TCPClient(queue)
	asyncore.loop()
	
if __name__ == '__main__':
	from multiprocessing import  Queue
	from time import time
	cola = Queue()
	init(cola)
	while True:
		tmp = time()
		data = cola.get()
		print("Tiempo: {0}".format(time()-tmp))
