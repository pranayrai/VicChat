import socket
import sys
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
from Client_data import client_data


class client_networking(QObject):
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

	@pyqtSlot()
	def run(self):
		self.s = socket.socket()
		host = socket.gethostname()
		port = 9999
		self.currentRoom = "general"
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
		while True:
			try:
				received = self.s.recv(1024)
				x = received.split(" ")
				if x[0] == "/roomlist":
					self.roomListSignal.emit(" ".join(str(i) for i in x[1:]))
				elif x[0] == "/history":
					room = x[1]
					# Attempt to add the chat room. If the room exists already,
					# this will return false and not change client_data
					if self.data.add_chatroom(room):
						self.join_room(room)
						continue
					y = " ".join(str(i) for i in x[2:])
					y = y.split('\n')
					for z in y:
						if z != '':
							self.data.add_message(z,room)
					#self.roomListSignal.emit(" ".join(str(i) for i in x[1:]))
				elif x[0] == "/error":
					self.errorSignal.emit(" ".join(str(i) for i in x[1:]))
				elif x[0] == "/sysmessage":
					self.greenSignal.emit(" ".join(str(i) for i in x[1:]))
				elif x[0] == self.currentRoom:
					msg = " ".join(str(i) for i in x[1:])
					self.data.add_message(msg,x[0])
					self.messageSignal.emit(msg)
				else:
					" ".join(str(i) for i in x[1:])
					self.data.add_message(msg,x[0])
					print "A message has been sent to another room:"
					print received

			except (socket.timeout):
				#No input received
				pass
			if self.z is not None:
				self.s.send(self.z)
				print self.z
				self.z = None

	def send_message(self,msg):
		self.s.send("/addmessage {} {}".format(self.currentRoom,msg))

	def create_room(self,msg):
		self.s.send("/createchatroom {}".format(msg))
		self.join_room(msg)

	def leave_room(self,msg):
		self.z = "/leavechatroom {}".format(msg)
		self.currentRoom = None
		self.data.remove_chatroom(msg)
		self.delRoomSignal.emit(msg)

	def join_room(self,msg):
		self.s.send("/joinchatroom {}".format(msg))
		self.currentRoom == msg
		self.joinRoomSignal.emit(self.currentRoom)
		self.data.add_chatroom(msg)

	def get_room_list(self):
		self.s.send("/listallrooms")

	def change_room(self,msg):
		self.currentRoom = msg
		hist = self.data.load_from_chatroom(msg)
		print hist
		return hist