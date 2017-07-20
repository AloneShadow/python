#!/usr/bin/python3

import os
from socket import *

sHost = ""
sPort = 12345

childList = []
msg_1 = "Message "
msg_2 = " from client.\n T "

def client_fork():
    print("Started child process: ", os.getpid())
    sockObj = socket(AF_INET, SOCK_STREAM)
    sockObj.connect((sHost, sPort))
    msg = (msg_1+str(0)+msg_2).encode()
    sockObj.send(msg)
    data = sockObj.recv(1024)
    print ("Server answered: ", data)
    sockObj.close()
    os._exit(0)

def main():
    childPid = os.fork()
    if childPid == 0: client_fork()
    else:
        print("Started child, pid: ", childPid)
        childList.append(childPid)

main()
