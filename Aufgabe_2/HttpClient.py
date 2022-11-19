#!/usr/bin/python3

# Um Sockets verwenden zu kÃ¶nnen, mÃ¼ssen wir das socket Modul importieren
import socket
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

scheme = sys.argv[1].split('://')
temp = scheme[1]
scheme.pop()
scheme += temp.split('/')

print("Das ist die Liste: ", scheme)
print("Das ist die Argument 2: ", sys.argv[2])

outputString = "GET {} HTTP/1.1\r\nhost: {} \r\n\r\n".format(sys.argv[1],scheme[1])
#outputString = "GET /wiki/Pinguine#/media/Datei:Falkland_Islands_Penguins_36.jpg HTTP/1.1\r\nhost: {} \r\n\r\n".format(scheme[1])


print("Send request to Server:\n", outputString)



try:
    # Wir erzeugen einen Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wir verbinden uns mit dem Server (Host: google.at, Port: 80)
    # Die doppelten runden Klammern sind kein Fehler, sonder wichtig!
    # connect() wird hier EIN EINZIGER Eingabeparameter Ã¼bergeben, ein sog. Tupel.
    # Das innere Klammernpaar bildet das Tupel.
    sock.connect((scheme[1], 80))
    #sock.connect(("www.google.at", 80))

    # Wir senden eine Anfrage an den Server
    # Python3 verwendet intern Unicode-Strings, Ã¼ber das Netzwerk kÃ¶nnen wir nur Byte-Strings schicken
    # daher mÃ¼ssen wir Python-String mit encode('<codec>') in einen Byte-String umwandeln
    sock.send(outputString.encode("utf-8"))

    # Wir empfangen die Antwort vom Server
    # Als BuffergrÃ¶ÃŸe verwenden wir 2048, wenn die Nachricht grÃ¶ÃŸer ist, mÃ¼ssen wir recv() mehrmals aufrufen
    response = sock.recv(2048)
    response += sock.recv(2048)
    response += sock.recv(2048)
    response += sock.recv(2048)
    response += sock.recv(2048)
    response += sock.recv(2048)

    # Wir geben die Antwort aus
    # Um einen Byte-String in einen Unicode-String umzuwandeln, mÃ¼ssen wir decode() aufrufen
    print(response.decode())

    original_stdout = sys.stdout  # Save a reference to the original standard output

    with open(sys.argv[2], 'w') as f:
        sys.stdout = f  # Change the standard output to the file we created.
        print(response.decode())
        sys.stdout = original_stdout  # Reset the standard output to its original value

    # Nicht vergessen alle Ressourcen wieder zu schlieÃŸen
    sock.close()

except:
    print("Ein Fehler ist aufgetreten")
    # Gebe die Exception und einen Stacktrace fÃ¼r die Fehlersuche aus
    import traceback

    traceback.print_exc()
