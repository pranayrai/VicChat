import socket
import sys
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
from Client_data import client_data


class Client(QObject):
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
	#roomList = []
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
		#This causes all socket operations on s to timeout (Throw a socket.timemout exception)
		#if more than the set time passes
		self.s.settimeout(0.01)

		#Continuously look for user and server messages
		while True:
			try:
				received = self.s.recv(1024)
				x = received.split(" ")
				if x[0] == "/roomlist":
					self.roomListSignal.emit(" ".join(str(i) for i in x[1:]))
				elif x[0] == "/history":
					self.greenSignal.emit("{} has been added to your list of rooms.".format(self.currentRoom))
					self.joinRoomSignal.emit(self.currentRoom)
					y = " ".join(str(i) for i in x[1:])
					y = y.split('\n')
					for z in y:
						if z != '':
							self.data.add_message(z,self.currentRoom)
				elif x[0] == "/error":
					self.errorSignal.emit(" ".join(str(i) for i in x[1:]))
				elif x[0] == "/display":
					self.greenSignal.emit(" ".join(str(i) for i in x[1:]))
				
				elif x[0] == self.currentRoom:
					self.data.add_message(" ".join(str(i) for i in x[1:]),x[0])
					self.messageSignal.emit(" ".join(str(i) for i in x[1:]))
				else:
					self.data.add_message(" ".join(str(i) for i in x[1:]),x[0])
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
		self.z = "/addmessage {} {}".format(self.currentRoom,msg)

	def create_room(self,msg):
		self.z = "/createchatroom {}".format(msg)
		#self.currentRoom = msg
		#self.data.add_chatroom(msg)

	def leave_room(self,msg):
		self.z = "/leavechatroom {}".format(msg)
		self.currentRoom = None
		self.data.remove_chatroom(msg)
		self.delRoomSignal.emit(msg)

	def join_room(self,msg):
		self.currentRoom = msg
		hist = self.data.load_from_chatroom(msg)
		if hist:
			return hist
		self.z = "/joinchatroom {}".format(msg)
		self.data.add_chatroom(msg)

	def get_room_list(self):
		self.z = "/listallrooms"
		#return self.data.list_chatrooms()

	def change_room(self,msg):
		self.currentRoom = msg
		return self.data.load_from_chatroom(msg)





# ---EVERYTHING BELOW HERE IS OLD AND NOT USED---








def check_for_input(self):
	print "checking input!"
	global z
	try:
		while True:
			z = raw_input("")
			#z = gui.gui_input()
			print z
	except KeyboardInterrupt:
		s.shutdown(socket.SHUT_RDWR)
		s.close()


def server_stuff():
	print "server running!"
	s = socket.socket()
	host = socket.gethostname()
	port = 9999

	try:
		s.connect((host, port))
	except:
		#gui.no_connection()
		print "could not connect A"
	print 'Connected to', host
	z = None

	#This causes all socket operations on s to timeout (Throw a socket.timemout exception)
	#if more than the set time passes
	s.settimeout(0.01)



	#Continuously look for user and server messages
	while True:
		'''try:
			#print '\n'+'\t'+'\t'+s.recv(1024)
			#gui.gui_output(None,s.recv(1024))
		except (socket.timeout):
			#No input received
			pass'''
		if z is not None:
			for i in z:
				s.send(z)
			z = None

if __name__ == "__main__":
	#Start the input method as a second thread
	print "START THE APP FROM THE GUI FOOL"
