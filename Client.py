import socket
import sys
import threading

s = socket.socket()
host = socket.gethostname()
port = 9999

s.connect((host, port))
print 'Connected to', host
z = None

while True:
	if z != None:
		print s.recv(1024)
		z = None
	z = raw_input("Enter something ")
	s.send(z)
    
    # Halts
    #print '[Waiting for response...]'