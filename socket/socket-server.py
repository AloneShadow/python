"""
simple server
"""

from socket import *

myHost = ""
myPort = 12345

sockObj = socket(AF_INET, SOCK_STREAM)
sockObj.bind((myHost, myPort))
sockObj.listen(2)

while True:
    connect, address = sockObj.accept()
    print("I've got :", connect, " from ", address)
    print ("Readind data from connection ", connect)
    while True:
        data = connect.recv(1024)
        if not data: break
        print ("Data: ", data.decode())
        print ("Send data back to client: ", b"You send me "+data)
        connect.send(b"You send me "+data)
    connect.close()