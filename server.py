import socket
import sys
import threading

s = socket.socket()
host = socket.gethostname()
port = 9999
s.bind((host, port))

s.listen(5)
c = None
c2 = None
if c is None:
	# Halts
	print '[Waiting for connection...]'
	c, addr = s.accept()
	print 'Got connection from', addr
		
if c2 is None:
	c2, addr2 = s.accept()
	print 'Got connection from', addr2
	
while True:	
	if c is not None:
		# Halts
		#print '[Waiting for response...]'
		
			#print 'receiving data from %s'%ad
			q = c.recv(1024)
			#q = raw_input("Enter something to this client: ")
			c2.send(q)
			

	if c2 is not None:
		# Halts
		#print '[Waiting for response...]'
		
			#print 'receiving data from %s'%ad
			q = c2.recv(1024)
			#q = raw_input("Enter something to this client: ")
			c.send(q)
			