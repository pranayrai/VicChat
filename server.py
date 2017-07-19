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
print('[Waiting for connection...]')
while c is None:
		c, addr = s.accept()
print 'Got connection from', addr
		
while c2 is None:
	c2, addr2 = s.accept()
print 'Got connection from', addr2

#This causes all socket operations on s to timeout (Throw a socket.timemout exception)
#if more than the set time passes.
c.settimeout(0.01)
c2.settimeout(0.01)

while True:
	q = None
	if c is not None:
		# Halts
		#print '[Waiting for response...]'
		
		#print 'receiving data from %s'%ad
		try:
			q = c.recv(1024)
			c2.send(q)
		except(socket.timeout):
			#If the socket times out, there isn't any input from c1
			pass
			
	if c2 is not None:
		# Halts
		#print '[Waiting for response...]'
	
		#print 'receiving data from %s'%ad
		try:
			q = c2.recv(1024)
			c.send(q)
		except(socket.timeout):
			#If the socket times out, there isn't any input from c2
			pass
			