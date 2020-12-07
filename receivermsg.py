import socket
import time

UDP_IP = "10.35.70.3"
UDP_Port= 33001
sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(UDP_IP, UDP_PORT)

while True:
    msg, addr= sock.recvfrom(1024)
    print (msg)
