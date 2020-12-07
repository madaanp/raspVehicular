import socket
import time

UDP_IP = "10.35.70.3"
UDP_Port= 33001
sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    v= input("Message: ")
    MESSAGE= str(v)
    sock.sendto(MESSAGE, (UDP_IP, UDP_Port))
