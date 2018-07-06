import asyncore
import socket

class TCPClient(asyncore.dispatcher):
    # BUFF_SIZE = 8*1024
    BUFF_SIZE = 8*1024*1024

    def __init__(self, queue):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(('127.0.0.1', 1234))
        self.queue = queue

    def writable(self):
        return 0 # don't have anything to write

    def handle_connect(self):
        pass # connection succeeded

    def handle_expt(self):
        self.close() # connection failed, shutdown

    def handle_read(self):
        s = self.recv(self.BUFF_SIZE)
        if len(s)>15:
            self.queue.put(s)

    def handle_close(self):
        self.close()


def init(queue):
    client = TCPClient(queue)
    asyncore.loop()
