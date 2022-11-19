#!/usr/bin/python
import signal
import socket
import logging
import sys
import threading
import curses
import time


sock_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = 'DISCOVER'
sock_UDP.bind(("", 5555))
sock_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock_UDP.sendto(msg.encode("utf-8"), ("255.255.255.255", 3333))
addr = sock_UDP.recvfrom(1024)[0].decode()
print("Reply:", addr)
sock_UDP.close()

clear = addr.split(' ')[1]
IP = clear.split(':')[0]
PORT = int(clear.split(':')[1])

print('IP: ' + IP)
print('PORT: {}'.format(PORT))

name = input("Please enter chat your chatname: ")

sock_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_TCP.connect((IP, 3454))
sock_TCP.send(b'CONNECT ' + name.encode("utf-8") + b'\r\n')
print("Send chatname to Server: ", name)
print(sock_TCP.recv(2048).decode())

'''
def connect(user):

    sock_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_TCP.connect((IP, PORT))
    sock_TCP.send(b'CONNECT ' + user.encode("utf-8") + b'\r\n')
    print("Send chatname to Server: ", user)
    print(sock_TCP.recv(2048).decode())

    return sock_TCP
'''

flag = True

def send():
    #temp_sock = connect(name)
    global flag
    while flag:

        inp = input("\nSend: ")
        if inp == "exit":
            flag = False
        sock_TCP.send(b'MSG ' + inp.encode("utf-8") + b'\r\n')
        #print("Send message to Server: ", inp)
    sock_TCP.close()
    print("Send socket closed")


def recv():
    #temp_sock = connect(name)
    while flag:

        data = sock_TCP.recv(2048).decode()
        if data == "":
            continue
        elif data.startswith("200"):
            continue
        else:
            print("\nReceive: ", data)

    sock_TCP.close()
    print("Recv socket closed")

def ping():
    sock_TCP.send(b'MSG ' + name.encode("utf-8") + b'\r\n')

def handler(signum, frame):
    global flag
    print("KeyboardInterrupt")
    flag = False
    sys.exit(0)


sendThread = threading.Thread(target=send)
recvThread = threading.Thread(target=recv)

signal.signal(signal.SIGINT,handler)

sendThread.daemon = True
recvThread.daemon = True

sendThread.start()
recvThread.start()

sendThread.join()
recvThread.join()




