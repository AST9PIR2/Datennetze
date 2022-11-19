#!/usr/bin/python3

import socket
import sys
import re
import traceback
import threading
import signal
from functools import partial
import os

BUFFER = 2048

noEnding = True



def UDPBroadcast():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = 'DISCOVER'
        sock.bind(("", 5555))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(msg.encode("utf-8"), ("255.255.255.255", 3333))
        addr = sock.recvfrom(1024)[0].decode()
        print("Reply:", addr)
        sock.close()
    except:
        print("Fehler1")
        sock.close()
        sys.exit(1)

    clear = addr.split(' ')[1]
    host = clear.split(':')[0]
    port = int(clear.split(':')[1])

    return host, port


def ChooseName():
    print("Benutzername eingeben")
    user = input("Benutzername: ")

    while user == "" or " " in user:
        print("No valid name!")
        user = input("Username: ")

    print(f"Name: {user}")
    return user


def ConnectToServer(host, port, user):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print("Error!")
        sys.exit()
    try:
        connection_message = (b'CONNECT ' + user.encode() + b'\r\n')
        sock.send(connection_message)
    except:
        print("Error")
        sock.close()
        sys.exit(1)

    return sock


def DisconnectFromServer(sock, user):
    split_message = (b'DISCONNECT ' + user.encode() + b'\r\n')
    sock.send(split_message)
    sock.close()



def SendMessage(sock):
    global noEnding
    while noEnding:

        neuerInput: ""

        while neuerInput == "" and noEnding:
            neuerInput = input("Eingabe: ")

        neueNachricht = (b'MSG' + neuerInput.encode() + b'\r\n')

        if noEnding:
            try:
                sock.send(neueNachricht)
            except:
                print("Fehler")
                os.kill(os.getpid(), signal.SIGINT)


def RecvMessage(sock):
    global noEnding
    while noEnding:

        try:

            antwort = sock.recv(BUFFER).decode()
            if antwort == "":
                continue

        except:
            print("Fehler")


def pingServer(sock, anwender):
    global noEnding
    if noEnding:

        neueNachricht = (b'PING ' + anwender.encode() + b'\r\n')

        if noEnding:
            try:
                sock.send(neueNachricht)
            except:
                print("Fehler")
            threading.Timer(5, pingServer, (sock, anwender,0)).start()


host, port = UDPBroadcast()
user = ChooseName()
chatSocket = ConnectToServer(host, port, user)

sendThread = threading.Thread(target=SendMessage(chatSocket))
recvThread = threading.Thread(target=RecvMessage(chatSocket))
pingThread = threading.Thread(target=pingServer(chatSocket, user))

signal.signal(signal.SIGINT, partial(chatSocket, sendThread, recvThread, pingThread, user))

sendThread.start()
recvThread.start()
pingThread.start()
