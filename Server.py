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


clients = []
database = server_database()

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


def listen_connections():
	s.listen(5)
	print('[Waiting for connection...]')
	while True:
		c, addr = s.accept()
		print 'Got connection from', addr
		threading.Thread(target = get_usernames, args=(c)).start()
		w = 'Connected. You can start chatting now!'
		c.send(w)



threading.Thread(target = listen_input).start()
threading.Thread(target = listen_connections).start()



def get_username(c):
	c.send("Enter a username")
	while True:
		q = c.recv(1024)
		if database.add_user(q, c):
			c.settimeout(0.001)
			clients.append((c, q))
			break
		c.send("Username invalid/already taken. Please try another username")


"""def reconnect(c3, addr3):
	s.settimeout(1)
	print('[Waiting for connection...]')
    #while True:
    #s.close()
	c3, addr3 = s.accept()
	print 'Got connection from', addr3
	c3.send(w)
	return c3, addr3"""



def update_clients(li, msg, arg):
	str = arg + " " + msg
	for item in li:
		try:
			item[1].send(str)
		except socket.error as e:
			database.remove_user(item[0])
			for cli in clients:
				if cli[0] == item[0]:
					clients.remove(cli)
					break


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
	cmd = input[1]
	arg = input[2]
	if cmd == "addmessage":
		list = database.add(input[3], arg)
		if list:
			update_clients(list, input[3], arg)
		else:
			c.send("The chat room does not exist")
	elif cmd == "joinchatroom":
		database.link_user_chatroom(c[0], arg)
	elif cmd == "leavechatroom":
		database.unlink_user_chatroom(c[0], arg)
	elif cmd == "createchatroom":
		database.add_chatroom(arg)
		database.link_user_chatroom(c[0], arg)
	else:
		c.send("Invalid command")
