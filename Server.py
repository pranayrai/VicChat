import socket
import sys
import threading
import time
import re
from Server_database import server_database
s = socket.socket()
host = socket.gethostname()
port = 9999
s.bind((host, port))

c = None
c2 = None
global c3 
global addr3
global clients = []
global database = server_database()

threading.Thread(target = listen_input).start()
threading.Thread(target = listen_connections).start()

def listen_connections()
	s.listen(5)
	print('[Waiting for connection...]')
	while True:
		c, addr = s.accept()
		clients.append(c)
		print 'Got connection from', addr
		threading.Thread(target = get_usernames, args=(c)).start()
		w = 'Connected. You can start chatting now!'
		c.send(w)
		

def get_username(c):
	c.send("Enter a username")
	while True:
		q = c.recv(1024)
		if database.add_user(q):
			c.settimeout(0.001)
			clients.append((c, q))
			break
		c.send("Username invalid/already taken. Please try another username")
		

def reconnect(c3, addr3):
	s.settimeout(1)
    print('[Waiting for connection...]')
    #while True:
    #s.close()
    c3, addr3 = s.accept()
    print 'Got connection from', addr3
    c3.send(w)
    return c3, addr3


#This causes all socket operations on s to timeout (Throw a socket.timemout exception)
#if more than the set time passes.
c.settimeout(1)
c2.settimeout(1)

def listen_input():
	while True:
		q = None
		for c, u in clients:
			try:
				q = c.recv(1024)
				process_message(c, q)
			except(socket.timeout):
				#If the socket times out, there isn't any input from c1
				pass
			except socket.error as e:
				print 'lost connection from', addr
				c.close()
				c, addr = reconnect(c, addr)
				c.settimeout(1)
		
def process_message(c, str):
	"""
	- check if the string starts with a /
	- there will always be atleast one argument
	- first string = word starting with / (command)
	"""
	input = re.search('^/([a-z]+) -([a-z]+) ?(.*)$', str) 
	if input is None:
		c.send("Incorrect input format")
	return 

			
