import socket
import sys
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
from Client_data import client_data

# The main class, which is called from the GUI.
class client_networking(QObject):

	# The many types of signals used to communicate with the GUI.
	# Each signals sends information to the GUI to a function.
	# All of the signals can carry a string as a parameter.
	messageSignal = pyqtSignal(str)
	errorSignal = pyqtSignal(str)
	roomListSignal = pyqtSignal(str)
	greenSignal = pyqtSignal(str)
	joinRoomSignal = pyqtSignal(str)
	delRoomSignal = pyqtSignal(str)

	z = None
	s = socket.socket()
	currentRoom = None
	joinedRooms = []
	data = client_data()

	# run() is called when the thread that holds client_networking first starts.
	# It is the main setup and the initial connection to the server.
	@pyqtSlot()
	def run(self):
		# Sets up the socket using the same values as the server.
		self.s = socket.socket()
		host = socket.gethostname()
		port = 9999
		self.currentRoom = "general"
		# Tries to connect to the server. If this fails, it sends an error to
		# the GUI, then shuts down. User must restart the GUI to try again.
		try:
			self.s.connect((host, port))
		except:
			self.errorSignal.emit("Could not connect to server.")
			return
		print 'Connected to', host
		self.z = None
		#This causes all socket operations on s to timeout (Throw a socket.timeout exception)
		#if more than the set time passes
		self.s.settimeout(1)
		self.receive()

	#Continuously look for user and server messages
	def receive(self):
		# The main part of client_networking runs forever in this while loop.
		# Since client_networking is called in a separate thread from the GUI,
		# it can run in this loop without freezing anything for the user.
		while True:
			try:
				# Checks to see if the server has sent anything.
				received = self.s.recv(1024)

				# Breaks apart the received message in order to check the contents
				x = received.split(" ")

				# If it is a list of rooms it immediately sends it to the GUI to be displayed.
				if x[0] == "/roomlist":
					self.roomListSignal.emit(" ".join(str(i) for i in x[1:]))

				# History of a new room. Stores the history in the data and then
				# sends the history of the room to the GUI's textbox.
				elif x[0] == "/history":
					room = x[1]
					# History should only be loaded for a new chatroom or an empty (just created)
					# room. Otherwise, discard the data
					if self.data.add_chatroom(room) or self.data.load_from_chatroom(room) == []:
						y = " ".join(str(i) for i in x[2:])
						y = y.split('\n')
						for z in y:
							if z != '':
								self.data.add_message(z,room)
								if room == self.currentRoom:
									self.messageSignal.emit(z)
									pass
						self.joinRoomSignal.emit(self.currentRoom)

				# When an error message is received it is immediately output in red.
				elif x[0] == "/error":
					self.errorSignal.emit(" ".join(str(i) for i in x[1:]))

				# Sysmessages are output in green.
				elif x[0] == "/sysmessage":
					self.greenSignal.emit(" ".join(str(i) for i in x[1:]))

				# If the message received is for the current room, it's saved
				# in the data and then output to the user.
				elif x[0] == self.currentRoom:
					msg = " ".join(str(i) for i in x[1:])
					self.data.add_message(msg,x[0])
					self.messageSignal.emit(msg)

				# Otherwise, the message is simply stored without being output.
				else:
					" ".join(str(i) for i in x[1:])
					self.data.add_message(msg,x[0])
					#print "A message has been sent to another room:"
					#print received

			except (socket.timeout):
				#No input received
				pass

			# z is a way of sending a signal to the server.
			# If z has a value, it is sent, otherwise the loop continues.
			if self.z is not None:
				self.s.send(self.z)
				print self.z
				self.z = None

	# Sends a standard message to the server, containing the roomname and message.
	def send_message(self,msg):
		self.s.send("/addmessage {} {}".format(self.currentRoom,msg))

	# Commands the server to create a new room.
	# Then calls join_room() to join the newly made room.
	def create_room(self,msg):
		self.s.send("/createchatroom {}".format(msg))
		# without a slight delay the /joinchatroom command gets merged with the /createchatroom command.
		time.sleep(0.01)
		self.join_room(msg)

	# Informs the server that the user has left a chatroom.
	# Then deletes chatroom from the data.
	def leave_room(self,msg):
		self.z = "/leavechatroom {}".format(msg)
		self.currentRoom = None
		self.data.remove_chatroom(msg)
		self.delRoomSignal.emit(msg)

	# Join an already existing chatroom.
	# Adds that chatroom to the data.
	def join_room(self,msg):
		self.s.send("/joinchatroom {}".format(msg))
		self.currentRoom == msg
		self.joinRoomSignal.emit(self.currentRoom)
		self.data.add_chatroom(msg)

	# Requests a list of rooms from the server.
	def get_room_list(self):
		self.s.send("/listallrooms")

	# Sends a room's history to the GUI when the user switches between joined rooms.
	def change_room(self,msg):
		self.currentRoom = msg
		hist = self.data.load_from_chatroom(msg)
		return hist
