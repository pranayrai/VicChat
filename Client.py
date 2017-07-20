import socket
import sys
import threading

#Continuously look for input as a second thread. Stash any results in global z
def check_for_input():
	global z
	try:
		while True:
			z = raw_input("")
	except KeyboardInterrupt:
		s.shutdown(socket.SHUT_RDWR)
		s.close()

	

s = socket.socket()
host = socket.gethostname()
port = 9999

s.connect((host, port))
print 'Connected to', host
z = None

#This causes all socket operations on s to timeout (Throw a socket.timemout exception)
#if more than the set time passes
s.settimeout(0.01)

#Start the input method as a second thread
threading.Thread(target = check_for_input).start()

#Continuously look for user and server messages
while True:
	try:
		print '\n'+'\t'+'\t'+s.recv(1024)
	except (socket.timeout):
		#No input received
		pass
	if z is not None:
		s.send(z)
		z = None
	
