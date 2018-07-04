import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


def send(bytes):
	sock.sendto(bytes, (UDP_IP, UDP_PORT))