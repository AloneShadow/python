#!/usr/bin/python3

"""
Multithreading server
"""

from socket import *
import os, time, signal, _thread

myHost = ""
myPort = 12345
childList = []

sockObj = socket(AF_INET, SOCK_STREAM)
sockObj.bind((myHost, myPort))
sockObj.listen(1)

def server_fork(connect):
 print("Child server is: ", os.getpid())
 time.sleep(5)
 while True:
    data = connect.recv(1024)
    if not data: break
    print ("Data: ", data.decode())
    print ("Send data back to client: ", b"You send me "+data)
    connect.send(b"You send me "+data)
 connect.close()

def server():
 print("I'm ready at: ",myHost,':',myPort)
 while True:
    connect, address = sockObj.accept()
    print("I've got :", connect, " from ", address)
    print ("Readind data from connection ", connect)
    _thread.start_new_thread(server_fork, (connect,))

server()
