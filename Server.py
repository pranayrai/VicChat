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
database.add_chatroom('general')


def listen_input():
	while True:
		q = None
		for cli in clients:
			try:
				q = cli[0].recv(1024)
				process_message(cli[0], cli[1], q)
			except(socket.timeout):
				#If the socket times out, there isn't any input from c1
				pass
			except socket.error:
				#If the socket throws an error, one of the clients has left
				#Remove that client from the list, so that we are no longer
				#listening for it
				database.remove_user(cli[1])
				print "User disconnected: " + cli[1]
				clients.remove(cli)


def listen_connections():
	s.listen(5)
	print('[Waiting for connections...]')
	while True:
		c, addr = s.accept()
		print 'Got connection from', addr
		threading.Thread(target = get_username, args=(c,)).start()

threading.Thread(target = listen_input).start()
threading.Thread(target = listen_connections).start()


def get_username(c):
	c.send("general Enter a username")
	try:
		while True:
			msg = c.recv(1024)
			y = msg.split()
			if len(y) < 3:
				c.send("/error Incorrect message format. Please update the client")
				continue
			name = str(y[2])
			if name and database.add_user(name, c):
				c.settimeout(0.001)
				clients.append((c, name))
				database.link_user_chatroom(name, 'general')
				break
			c.send("/error Username already exists. Try a different username")
		c.send('/roomlist' + database.list_chatrooms())
		time.sleep(0.1)
		c.send('general Connected to "general." You can start chatting now!')
		time.sleep(0.1)
		c.send("/history " + database.chatroom_history('general'))
	except socket.error:
		pass


def update_clients(li, msg):
	for item in li:
		try:
			item[0].send(msg)
		except socket.error as e:
			database.remove_user(item[0])
			clients.remove(item)
			print "User disconnected: " + u


def process_message(c, username, msg):
	"""
	- check if the string starts with a /
	- there will always be atleast one argument
	- first string = word starting with / (command)
	"""
	y = msg.split()
	if len(y) < 1:
		c.send("/error Incorrect message format. Please update the client")
		return
	elif len(y) < 2:
		cmd = str(y[0])
		if cmd is None:
			c.send("/error Incorrect input format")
		elif cmd == "listallrooms":
			c.send('/roomlist' + database.list_chatrooms())
	else:
		cmd = str(y[0])
		arg = str(y[1])
		text = ""
		for i in range (2,len(y),1):
			text += str(y[i]) + " "
		print cmd, arg, text
		if cmd is None:
			c.send("/error Incorrect input format")
			return
		if cmd == "/addmessage":
			messageText = username + ": " + text
			li = database.add_message(messageText, arg)
			if li:
				update_clients(li, arg + " " + messageText)
			else:
				c.send("The chat room does not exist")
		elif cmd == "/joinchatroom":
			database.link_user_chatroom(username, arg)
			c.send("/history " + database.chatroom_history(arg))
		elif cmd == "/leavechatroom":
			database.unlink_user_chatroom(username, arg)
		elif cmd == "/createchatroom":
			database.add_chatroom(arg)
			database.link_user_chatroom(username, arg)
			update_clients(clients, "/roomlist " + arg)
		else:
			c.send("/error Invalid command")
