#!/usr/bin/python3

# Um Sockets verwenden zu kÃ¶nnen, mÃ¼ssen wir das socket Modul importieren
import socket
import sys
import re

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

scheme = sys.argv[1].split('://')
temp = scheme[1]
scheme.pop()
scheme += temp.split('/')

print("Das ist die Liste: ", scheme)
print("Das ist die Argument 2: ", sys.argv[2])

print("Das ist die scheme 2: ", scheme[2])
print("Das ist die scheme 1: ", scheme[1])

outputString = 'GET /{} HTTP/1.1 \r\nhost: {} \r\n\r\n'.format(scheme[2],scheme[1])
#outputString = 'GET /cover3.jpg HTTP/1.1\r\nHOST: data.pr4e.org\r\n\r\n'


print("Send request to Server:\n", outputString)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Wir erzeugen einen Socket
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wir verbinden uns mit dem Server (Host: google.at, Port: 80)
    # Die doppelten runden Klammern sind kein Fehler, sonder wichtig!
    # connect() wird hier EIN EINZIGER Eingabeparameter Ã¼bergeben, ein sog. Tupel.
    # Das innere Klammernpaar bildet das Tupel.
    sock.connect((scheme[1], 2500))
    #sock.connect(("data.pr4e.org", 80))

    # Wir senden eine Anfrage an den Server
    # Python3 verwendet intern Unicode-Strings, Ã¼ber das Netzwerk kÃ¶nnen wir nur Byte-Strings schicken
    # daher mÃ¼ssen wir Python-String mit encode('<codec>') in einen Byte-String umwandeln
    sock.send(outputString.encode("utf-8"))
    #sock.send('GET http://data.pr4e.org/cover3.jpg HTTP/1.1\n\n')

    # Wir empfangen die Antwort vom Server
    # Als BuffergrÃ¶ÃŸe verwenden wir 2048, wenn die Nachricht grÃ¶ÃŸer ist, mÃ¼ssen wir recv() mehrmals aufrufen
    response = sock.recv(1024)

    for i in range(0, 1):
        response += sock.recv(2048)

    
    # Wir geben die Antwort aus
    # Um einen Byte-String in einen Unicode-String umzuwandeln, mÃ¼ssen wir decode() aufrufen
    #print(response.decode())

    #original_stdout = sys.stdout  # Save a reference to the original standard output
    with open(sys.argv[2], 'wb') as f:
        #sys.stdout = f  # Change the standard output to the file we created.
        #f.write(response.decode(encoding='UTF-8',errors='ignore').split('Content-Type: image/jpeg')[1])

        #REGEX for jpg
        #x = re.search(b"(?s)(?<=image/jpeg)(.*$)", response)
        #var = x.group().split(b"\r\n\r\n")[1]
        try:
            print(response.decode())
            #feedback = response.split(b'\r\n\r\n')[0]
            var = response.split(b'\r\n\r\n')[1]
            #print(feedback.decode())
            f.write(var)
            #f.write(response)
        except:
            print(response.decode())


        #sys.stdout = original_stdout  # Reset the standard output to its original value


    # Nicht vergessen alle Ressourcen wieder zu schlieÃŸen
    sock.close()

except:
    print("Ein Fehler ist aufgetreten")
    sock.close()
    # Gebe die Exception und einen Stacktrace fÃ¼r die Fehlersuche aus
    import traceback

    traceback.print_exc()
