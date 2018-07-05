import asyncore
import socket
import numpy as np

class TCPClient(asyncore.dispatcher):
    BUFF_SIZE = 8192*1024

    def __init__(self, queue):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(('127.0.0.1', 1234))
        self.queue = queue
        self.buffer = bytearray()

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
        	if len(self.buffer)>=self.BUFF_SIZE:
        		self.queue.put(self.complex_array(self.buffer))
        		self.buffer = bytearray()

    def handle_close(self):
        self.close()


def init(queue):
	request = TCPClient(queue)
	asyncore.loop()