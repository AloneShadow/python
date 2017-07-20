#!/usr/bin/python3

"""
Multiprocess server
"""

from socket import *
import os, time, signal

myHost = ""
myPort = 12345
childList = []

sockObj = socket(AF_INET, SOCK_STREAM)
sockObj.bind((myHost, myPort))
sockObj.listen(2)
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

def server_fork(connect):
 print("Child server is: ", os.getpid())
 time.sleep(15)
 while True:
    data = connect.recv(1024)
    if not data: break
    print ("Data: ", data.decode())
    print ("Send data back to client: ", b"You send me "+data)
    connect.send(b"You send me "+data)
 connect.close()
 os._exit(0)

def server():
 print("I'm ready at: ",myHost,':',myPort)
 while True:
    connect, address = sockObj.accept()
    print("I've got :", connect, " from ", address)
    print ("Readind data from connection ", connect)
    childPid = os.fork()
    if childPid == 0: server_fork(connect)
    else: childList.append(childPid)


server()
