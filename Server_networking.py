import socket
import sys
import threading
import time
from Server_data import server_data

s = socket.socket()
host = socket.gethostname()
port = 9999
s.bind((host, port))

clients = []
data = server_data()
data.add_chatroom('general')


def receive():
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
				data.remove_user(cli[1])
				print "User disconnected: " + cli[1]
				clients.remove(cli)


def listen_connections():
	s.listen(5)
	print('[Waiting for connections...]')
	while True:
		c, addr = s.accept()
		print 'Got connection from', addr
		threading.Thread(target = get_username, args=(c,)).start()

threading.Thread(target = receive).start()
threading.Thread(target = listen_connections).start()


def get_username(c):
	c.send("/sysmessage Enter a username")
	try:
		while True:
			msg = c.recv(1024)
			y = msg.split()
			if len(y) < 3:
				c.send("/error Incorrect message format. Please update the client")
				continue
			name = str(y[2])
			rooms = data.add_user(name, c)
			if name and rooms:
				c.settimeout(0.001)
				clients.append((c, name))
				if type(rooms) is list:
					for r in rooms:
						c.send("/history " + r + " " + data.chatroom_history(r))
				else:
					data.link_user_chatroom(name, 'general')
					c.send("/history general " + data.chatroom_history('general'))
				break
			c.send("/error Username already exists. Try a different username")
	#If the user doesn't complete the login process, don't add them to the list of users
	except socket.error:
		pass


def update_clients(li, msg):
	for item in li:
		try:
			item[0].send(msg)
		except socket.error as e:
			data.remove_user(item[1])
			print "User disconnected: " + item[1]


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
		elif cmd == "/listallrooms":
			c.send('/roomlist' + data.list_chatrooms())
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
			li = data.add_message(messageText, arg)
			if li:
				update_clients(li, arg + " " + messageText)
			else:
				c.send("/error The chat room does not exist")
		elif cmd == "/joinchatroom":
			data.link_user_chatroom(username, arg)
			hist = data.chatroom_history(arg)
			if hist:
				c.send("/history " + arg + " " + hist)
		elif cmd == "/leavechatroom":
			data.unlink_user_chatroom(username, arg)
		elif cmd == "/createchatroom":
			data.add_chatroom(arg)
			data.link_user_chatroom(username, arg)
			#update_clients(clients, "/roomlist " + arg)
		else:
			c.send("/error command not recognized")
