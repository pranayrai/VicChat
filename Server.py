import socket
import sys
import threading
import time

s = socket.socket()
host = socket.gethostname()
port = 9999
s.bind((host, port))

s.listen(5)
c = None
c2 = None
c3 = None
print('[Waiting for connection...]')
while c is None:
		c, addr = s.accept()
print 'Got connection from', addr
w = 'Connected. You can start chatting now!'
c.send(w)
		
while c2 is None:
	c2, addr2 = s.accept()
print 'Got connection from', addr2
c2.send(w)

def reconnect():
    toBreak = False
    while True:
        s.close()
        c3, addr3 = s.accept()
        print 'Got connection from', addr3
        toBreak = True       
        if toBreak:
            break
    	time.sleep(1)


#This causes all socket operations on s to timeout (Throw a socket.timemout exception)
#if more than the set time passes.
c.settimeout(0.01)
c2.settimeout(0.01)

while True:
	try:
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
	except socket.error as e:
		print 'lost connection from', addr
		reconnect()
		
	try:	
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
	except socket.error as e:
		print 'Lost connection from', addr2
		reconnect()
			
