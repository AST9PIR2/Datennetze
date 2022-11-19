#!/usr/bin/python3

# Wird benÃ¶tigt, damit wir Sockets verwenden kÃ¶nnen
import socket
import datetime
import os
import platform
import sys


import datetime as datetime

TCP_IP = 'localhost'
TCP_PORT = 2500
BUFFER_SIZE = 2048

'''
HTTP/1.1 200 OK
Date: Mon, 07 Nov 2022 16:29:43 GMT
Server: Apache/2.4.18 (Ubuntu)
Last-Modified: Mon, 15 May 2017 12:27:40 GMT
ETag: "38342-54f8f2e5b6277"
Accept-Ranges: bytes
Content-Length: 230210
Vary: Accept-Encoding
Cache-Control: max-age=0, no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: Wed, 11 Jan 1984 05:00:00 GMT
Content-Type: image/jpeg
'''
error = b'HTTP/1.1 400 Bad Request\r\n'
no_error = b'HTTP/1.1 200 OK\r\n'
date = b'Date: '+ datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT").encode("utf-8") + b'\r\n'
server = b'Server: '+ platform.platform().encode("utf-8") + b'\r\n\r\n'

badRequest = error + date + server
okRequest = no_error + date + server
print(date.decode() + server.decode())


# Wir erzeugen einen neuen Stream Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.close()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Wir binden den Socket an eine IP und einen Port,
# und machen ihn dadurch zu einem Server-Socket
sock.bind((TCP_IP, TCP_PORT))

# Wir warten auf eingehende Verbindungen
sock.listen()

# Wir akzeptieren eine eingehende Verbindung
clientsock, clientaddr = sock.accept()
print('Eingehende Verbindung von ', clientaddr)
try:
    while True:
        # Wir empfangen Daten vom Client
        data = clientsock.recv(2048)
        clientRequest = data.split(b' ')[0].decode()
        requestedFile = sys.argv[1] + data.split(b' ')[1].decode()
        print('Http: ' + data.split(b' ')[2].decode())


        if (clientRequest == 'GET') and (data.split(b' ')[2].decode() == 'HTTP/1.1'):
            print("Das ist ein GET")
            #clientsock.send(okRequest + data)
            #clientsock.close()
            print(sys.argv[1])

            if os.path.isfile(requestedFile):
                print("Datei existiert")
                file = open(requestedFile, "rb")
                buffer = file.read()
                file.close()
                clientsock.send(okRequest + buffer)
                clientsock.close()
            else:
                print("Datei existiert nicht")
                file = open(sys.argv[1] + '404.html', "rb")
                buffer = file.read()
                file.close()
                clientsock.send(buffer)
                clientsock.close()

        else:
            print("Das ist kein GET")
            clientsock.send(badRequest)
            clientsock.close()
            break

        print("Empfangene Daten: ", data)

        # Wir senden die Daten zurÃ¼ck an den Client
        #clientsock.send(data )
        #clientsock.send(404.html)
    # Wir geben alle Ressourcen wieder frei
    clientsock.close()
    sock.close()
except:
    file = open(sys.argv[1] + '500.html', "rb")
    buffer = file.read()
    file.close()
    #clientsock.send(buffer)
    clientsock.close()
    sock.close()
