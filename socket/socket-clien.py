from socket import *

sHost = ""
sPort = 12345


msg_1 = "Message "
msg_2 = " from client.\n T "
counter = 1

while True:
    sockObj = socket(AF_INET, SOCK_STREAM)
    sockObj.connect((sHost, sPort))
    msg = (msg_1+str(counter)+msg_2).encode()
    sockObj.send(msg)
    counter += 1
    data = sockObj.recv(1024)
    print ("Server answered: ", data)
    sockObj.close()