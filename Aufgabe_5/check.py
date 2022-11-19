#!/usr/bin/python
import socket
import logging
import threading
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = 'DISCOVER'
sock.bind(("", 5555))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(msg.encode("utf-8"), ("255.255.255.255", 3333))
addr = sock.recvfrom(1024)[0].decode()
print("Reply:", addr)
sock.close()

clear = addr.split(' ')[1]
IP = clear.split(':')[0]
PORT = int(clear.split(':')[1])

print('IP: ' + IP)
print('PORT: {}'.format(PORT))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PORT))
s.listen(1)
try:
    while True:
        komm, addr = s.accept()
        while True:
            data = komm.recv(1024)
            if not data:
                komm.close()
                break
            print("[{}] {}".format(addr[0], data.decode()))
            nachricht = input("Antwort: ")
            komm.send(nachricht.encode())
finally:
    s.close()