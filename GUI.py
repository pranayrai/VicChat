import sys
import threading
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from time import sleep
from Client_networking import client_networking
from functools import partial

# A class which creates a list of all rooms, called in room_list()
class RoomListWindow(QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)

# The main window, the entire visible GUI will be contained within this class.
class GUIWindow(QWidget):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		# Name and resize the main window
		self.setWindowTitle('VicChat GUI prototype')
		self.resize(320, 310)

		# Create the send message button
		self.btn = QPushButton('Print text to console', self)

		# Create textbox for data-entry
		self.inputBox = QLineEdit(self)
		self.inputBox.setPlaceholderText("enter message here")

		# Create a multi-line textbox to display history
		self.outputBox = QTextEdit(self)
		self.outputBox.setReadOnly(True)

		# Add the room label
		self.roomLabel = QLabel(self)
		self.roomLabel.setText("Room: ")

		# Create combobox for room list
		self.rooms = QComboBox(self)

		# Button to add a new room
		self.addRoomBtn = QPushButton('New Room', self)
		self.addRoomBtn.setToolTip('Click to create a new room')

		# Button that calls window with list of all rooms.
		self.roomListBtn = QPushButton('Room List', self)
		self.roomListBtn.setToolTip('Click to show list of rooms')

		# Place everything on the screen using a layout
		self.layout = QVBoxLayout()

		# Create a horizontal layout for the label and 2 buttons along the top
		self.topL = QHBoxLayout()
		self.topL.addWidget(self.roomLabel)
		self.topL.addWidget(self.rooms)
		self.topL.addWidget(self.roomListBtn)
		self.topL.addStretch()
		self.topL.addWidget(self.addRoomBtn)

		# Put the HLayout and the 3 remaining widgets into the main layout
		self.layout.addLayout(self.topL)
		self.layout.addWidget(self.outputBox)
		self.layout.addWidget(self.inputBox)
		self.layout.addWidget(self.btn)

		# Connect the layout to the main window
		self.setLayout(self.layout)


		# SET UP THE CLIENT IN A NEW THREAD:
		self.client = client_networking()
		self.thread = QThread(self)

		# Signal for GUI to display a standard message
		self.client.messageSignal.connect(self.receive_info)

		# Signal for the GUI to open the list of rooms
		self.client.roomListSignal.connect(self.room_list)

		# Error signal from the client (red text)
		self.client.errorSignal.connect(self.error_output)

		# Signal to display green text
		self.client.greenSignal.connect(self.green_output)

		# Signal to add a new room to the GUI's QComboBox
		self.client.joinRoomSignal.connect(self.join_room)

		# Signal to remove a room from the GUI's QCombobox
		self.client.delRoomSignal.connect(self.delete_room)

		# Move the new client instance onto the QThread
		self.client.moveToThread(self.thread)
		self.thread.started.connect(self.client.run)

		# Connect the buttons/input to their functions:
		self.inputBox.returnPressed.connect(self.on_press_print)
		self.btn.pressed.connect(self.on_press_print)
		self.rooms.currentIndexChanged.connect(self.change_room)
		self.addRoomBtn.clicked.connect(self.new_room)

		# When the Room List button is pressed, instead of immediately opening
		# the new window, it instead sends a signal to the client to request
		# a list of rooms from the server. Once that list returns, it then
		# opens the Room List window using the list of rooms recieved.
		self.roomListBtn.clicked.connect(lambda: self.client.get_room_list())

		# Start the thread!
		self.thread.start()

	# This is called when the new room button is pressed
	@pyqtSlot()
	def new_room(self):
		# Creates a pop-up window with a textbox
		text, ok = QInputDialog.getText(self, 'Create new room', 'Enter a room name:')
		if ok:
			# Checks for spaces which can mess up the list of rooms.
			if ' ' in text:
				self.error_output("Chatroom names cannot contain spaces.")
				return
			else:
				# Adds the room the the combobox and sends the name to the client.
				self.rooms.addItem(text)
				self.rooms.setCurrentIndex(self.rooms.count() - 1)
				self.client.create_room(text)

	# This is called when the room selection is changed
	@pyqtSlot()
	def change_room(self):
		self.outputBox.clear()
		hist = self.client.change_room(self.rooms.currentText())
		if self.rooms.count() < 1:
			self.outputBox.append("<span style=\" color:#ff0000;\" >You are not in any rooms!</span>")
			return
		self.outputBox.append(
			"<span style=\" color:#008000;\" >Now chatting in {}.</span>".format(self.rooms.currentText()))
		if hist is not False:
			for i in hist:
				self.outputBox.append(i)

	# Sends the message to the server, then clears the inputBox.
	# Called when enter key is pressed or the send button is pressed.
	@pyqtSlot()
	def on_press_print(self):
		self.client.send_message(self.inputBox.text())
		self.inputBox.clear()


	# Receive messages from the server and display them to chat.
	@pyqtSlot(str)
	def receive_info(self, msg):
		self.outputBox.append(msg)

	# Receive messages from the server and display them to chat in green.
	@pyqtSlot(str)
	def green_output(self, msg):
		self.outputBox.append("<span style=\" color:#008000;\" >{}</span>".format(msg))

	# Receive messages from the server and display them to chat in red.
	@pyqtSlot(str)
	def error_output(self, msg):
		self.outputBox.append("<span style=\" color:#ff0000;\" >{}</span>".format(msg))

	# Takes a list of rooms and puts them on the QComboBox.
	@pyqtSlot(str)
	def get_new_room(self, roomList):
		roomList = roomList.split(' ')
		for i in roomList:
			self.rooms.addItem(i)

	# Called when a new room from the list is joined.
	@pyqtSlot(str)
	def join_room(self, room):
		joinedRooms = [self.rooms.itemText(i) for i in range(self.rooms.count())]
		if room not in joinedRooms:
			self.rooms.addItem(room)
			self.client.join_room(room)
		# Tries to close the room list window if it is open.
		try:
			self.nd.hide()
		except:
			return

	# Called when the client leaves a room, deleting the room from the GUI as well.
	@pyqtSlot(str)
	def delete_room(self, room):
		self.rooms.removeItem(self.rooms.findText(room))
		self.nd.hide()

	# Creates a new window with a list of all rooms, joined or not.
	@pyqtSlot(str)
	def room_list(self, roomList):
		# Sets up a new window named nd using the RoomListWindow class.
		self.nd = RoomListWindow()
		self.rlayout = QVBoxLayout()

		# Set up the list of rooms for them to be iterated through
		roomList = roomList.split("\n")[1:]
		# Create a list of rooms that have already been joined.
		joinedRooms = [self.rooms.itemText(i) for i in range(self.rooms.count())]

		# Create the list of rooms, each with either a join or leave button.
		buttons = []
		for i in roomList:
			tempLayout = QHBoxLayout()
			name = QLabel(self)
			name.setText(i)
			if i in joinedRooms:
				# Creates a button that calls leave_room(i)
				buttons.append(QPushButton("Leave", self.nd))
				buttons[-1].clicked.connect(partial(self.leave_room, data=i))
			else:
				# Creates a button that calls join_room(i)
				buttons.append(QPushButton("Join", self.nd))
				buttons[-1].clicked.connect(partial(self.join_room, room=i))
			tempLayout.addWidget(name)
			tempLayout.addWidget(buttons[-1])
			self.rlayout.addLayout(tempLayout)
		# Add the layout to the window and show the window.
		self.nd.setLayout(self.rlayout)
		self.nd.show()

	# When the Leave button is pressed, tells the client we are leaving the room.
	def leave_room(self, data="\n"):
		self.client.leave_room(data)


if __name__ == "__main__":

	# Create the application
	app = QApplication(sys.argv)

	# Choose a theme
	app.setStyle(QStyleFactory.create("plastique"))

	#Create and run the GUI window.
	gui = GUIWindow()
	gui.show()
	app.exec_()
