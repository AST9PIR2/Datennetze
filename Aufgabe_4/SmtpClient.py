import socket
import sys

IP_Address = '127.0.0.1'

file = open(sys.argv[4], "rb")
buffer = file.read().decode()
file.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP_Address, 25))

errormessage4XX = 'Warning! The command was not accepted, and the requested action did ' \
                  'not occur. However, the error condition is temporary, and the action may be requested again.' \
                  'Trying to resend the message, it might work.....'

errormessage5XX = 'ERROR! The command was not accepted, and the requested action did not occur.' \

HELO = 'HELO {}\r\n'.format('mail.google.com')
#HELO = 'HELO {}\r\n'.format(sys.argv[1])
MAIL_FROM = 'MAIL FROM: {}\r\n'.format(sys.argv[1])
RCPT_TO = 'RCPT TO: {}\r\n'.format(sys.argv[2])
DATA = 'DATA\r\nSubject: {}\r\nTo: {}\r\nFrom: {}\r\n\r\n{}\r\n.\r\n'.format(sys.argv[3],sys.argv[2],sys.argv[1],buffer)
QUIT = 'QUIT\r\n'

output = [HELO, MAIL_FROM, RCPT_TO, DATA, QUIT]
counter = 0

try:
    for i in output:
        print(i)
        sock.send(i.encode("utf-8"))
        buffer = sock.recv(1024).decode()
        if buffer.startswith('4'):
            print(errormessage4XX)
            while buffer.startswith('4'):
                sock.send(i.encode("utf-8"))
                buffer = sock.recv(1024).decode()
                counter += 1
                if counter == 3:
                    print(errormessage5XX)
                    break
            counter = 0
        elif buffer.startswith('5'):
            print(errormessage5XX)
            exit(1)
        else:
            print('\t'+ buffer)

except socket.error:
    print('Something went terribly wrong! Program will now exit!')

sock.close()
