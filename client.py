import socket
import threading

sock = socket.socket()
ip = "127.0.0.1"    # means local
port = 60000
sock.connect((ip, port))
i = 0
while True:
    sock.send(str(i))
    i+=1
