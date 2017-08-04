import socket
import sys
import threading
import time
from Server_data import server_data
from datetime import datetime

s = socket.socket()
host = socket.gethostname()
port = 9999
s.bind((host, port))

# clients will store a list of tuples (socket, username) corresponding to all active users
clients = []
# data holds all chat room and user objects
data = server_data()
# Initialize a general chatroom. This will be the default chatroom
data.add_chatroom('general')

# Continuously listen for input from clients
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

# Continuously listen for new clients
def listen_connections():
	s.listen(5)
	print('[Waiting for connections...]')
	while True:
		c, addr = s.accept()
		print 'Got connection from', addr
		threading.Thread(target = get_username, args=(c,)).start()

threading.Thread(target = receive).start()
threading.Thread(target = listen_connections).start()

# Once a new client connects, this method is started in a new thread
# This prevents one user from preventing other users from joining by stalling here
def get_username(c):
	c.send("/sysmessage Enter a username")
	try:
		while True:
			msg = c.recv(1024)
			y = msg.split()
			if len(y) < 3:
				# If this block runs, the client_networking is sending poorly
				# constructed messages
				c.send("/error Incorrect message format. Please update the client")
				continue
			name = str(y[2])
			rooms = data.add_user(name, c)
			if name and rooms:
				#If there is a list of rooms, the user is a permanent user
				#Send them the history of all of these rooms.
				c.settimeout(0.001)
				clients.append((c, name))
				if type(rooms) is list:
					for r in rooms:
						c.send("/history " + r + " " + data.chatroom_history(r))
				else:
					# If the user is a guest, put them in the general chatroom
					data.link_user_chatroom(name, 'general')
					c.send("/history general " + data.chatroom_history('general'))
				break
			c.send("/error Username already exists. Try a different username")
	#If the user doesn't complete the login process, don't add them to the list of users
	except socket.error:
		pass

# Send a message to all clients in a list
# li is a list of tuples: (socket, username)
def update_clients(li, msg):
	for item in li:
		try:
			item[0].send(msg)
		except socket.error as e:
			data.remove_user(item[1])
			print "User disconnected: " + item[1]

#Process user input, and send it where required (database, update clients, etc...)
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
			#Timestamp the message, then add the username who sent it
			time = str(datetime.now())
			time = time[11:16]
			messageText = time + " " + username + ": " + text
			li = data.add_message(messageText, arg)
			if li:
				# Distribute the message to all connected clients
				update_clients(li, arg + " " + messageText)
			else:
				#If data.add_message doesn't return a list, the chat room doesn't exist
				c.send("/error The chat room does not exist")
		elif cmd == "/joinchatroom":
			#Link the user to a chatroom, and send them that chatroom's history
			data.link_user_chatroom(username, arg)
			hist = data.chatroom_history(arg)
			if hist:
				c.send("/history " + arg + " " + hist)
		elif cmd == "/leavechatroom":
			#Remove a user from a chatroom
			data.unlink_user_chatroom(username, arg)
		elif cmd == "/createchatroom":
			#Create a new chatroom, and add the user to it
			data.add_chatroom(arg)
			data.link_user_chatroom(username, arg)
		else:
			c.send("/error command not recognized")
