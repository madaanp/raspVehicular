import socket
import time

UDP_IP = "10.35.70.38"
UDP_Port= 5005
sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    v= raw_input("Message: ")
    MESSAGE= str(v)
    sock.sendto(MESSAGE, (UDP_IP, UDP_Port))
