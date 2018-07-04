import asyncore
import socket, time
import numpy as np
import struct

# reference time (in seconds since 1900-01-01 00:00:00)
# TIME1970 = 2208988800L # 1970-01-01 00:00:00


class TCPClient(asyncore.dispatcher):
    # time requestor (as defined in RFC 868)

    # BUFF_SIZE = 8192*1024
    BUFF_SIZE = 4096

    def __init__(self, callback):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(('127.0.0.1', 1234))
        self.callback = callback
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
            # print("Tiempo de muestreo: {0}".format((time.time()-self.time)))
            self.time = time.time()
            self.callback(self.complex_array(s))

    def handle_close(self):
        self.close()


def init(callback):
	request = TCPClient(callback)
	asyncore.loop()