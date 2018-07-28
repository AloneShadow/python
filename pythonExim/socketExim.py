#!/bin/python

import socket

sock = socket.socket()
sock.connect(('example.org', 25))
sock.send('EHLO abc')
data = sock.recv(1024)
sock.close()

print data
