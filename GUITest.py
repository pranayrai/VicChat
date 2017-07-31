#Simple proof of concept GUI

import sys
import threading
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from time import sleep
from Client import Client
from functools import partial

class RoomListWindow(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

class GUIWindow(QWidget):
    # This is called when the new room button is pressed
    @pyqtSlot()
    def new_room(self):
        text, ok = QInputDialog.getText(self, 'Create new room', 'Enter a room name:')
        if ok:
            #self.rooms.addItem(text)
            #self.rooms.setCurrentIndex(self.rooms.count()-1)
            self.client.create_room(text)
            #self.client.leave_room(self.currentRoom)
            #self.client.join_room(self.rooms.currentText())
            #self.currentRoom = self.rooms.currentText()
        #self.commands.append("New room: " + text)

    # This is called when the room selection is changed
    @pyqtSlot()
    def change_room(self):
        #self.client.leave_room(self.currentRoom)
        self.outputBox.clear()
        hist = self.client.change_room(self.rooms.currentText())
        if self.rooms.count() < 1:
            self.outputBox.append("<span style=\" color:#ff0000;\" >You are not in any rooms!</span>")
            return
        self.outputBox.append("<span style=\" color:#008000;\" >Now chatting in {}.</span>".format(self.rooms.currentText()))
        if hist is not False:
            for i in hist:
                self.outputBox.append(i)

        '''self.client.join_room(self.rooms.currentText())
        self.outputBox.clear()
        self.currentRoom = self.rooms.currentText()'''

    # Sends the message to the server, then clears the inputBox.
    @pyqtSlot()
    def on_press_print(self):
        self.client.send_message(self.inputBox.text())
        self.inputBox.clear()


    def change_windows(self):
        self.login.hide()
        #self.app.setStyle(QStyleFactory.create(themeList.currentText()))
        self.username = self.nameInput.text()
        self.show()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.username = ''
        self.currentRoom = ''

        '''self.login = QWidget()
        loginLayout = QVBoxLayout()
        nameLabel = QLabel(self.login)
        nameLabel.setText("Enter a Username:")
        loginLayout.addWidget(nameLabel)
        self.nameInput = QLineEdit(self.login)
        self.nameInput.setPlaceholderText("enter name here")
        loginLayout.addWidget(self.nameInput)

        themeLabel = QLabel(self.login)
        themeLabel.setText("Choose a theme:")
        loginLayout.addWidget(themeLabel)
        themeList = QComboBox(self.login)
        themeList.addItems(QStyleFactory.keys())
        loginLayout.addWidget(themeList)
        # find current style
        index = themeList.findText(
                    qApp.style().objectName(),
                    Qt.MatchFixedString)
        # set current style
        themeList.setCurrentIndex(index)

        loginButton = QPushButton('Login', self.login)
        loginLayout.addWidget(loginButton)
        self.login.setLayout(loginLayout)

        self.login.show()
        loginButton.pressed.connect(self.change_windows)
        self.nameInput.returnPressed.connect(self.change_windows)'''


        # Name and resize the main window
        self.setWindowTitle('VicChat GUI prototype')
        self.resize(320,310)

        # Create the output button
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
        #self.rooms.addItem("general")
        #self.rooms.addItem("Random")

        # Button to add a new room
        self.addRoomBtn = QPushButton('New Room', self)
        self.addRoomBtn.setToolTip('Click to create a new room')

        self.roomListBtn = QPushButton('Room List', self)
        self.roomListBtn.setToolTip('Click to show list of rooms')

        #Place everything on the screen using a layout
        self.layout = QVBoxLayout()
        self.topL = QHBoxLayout()
        self.topL.addWidget(self.roomLabel)
        self.topL.addWidget(self.rooms)

        self.topL.addWidget(self.roomListBtn)
        self.topL.addStretch()
        self.topL.addWidget(self.addRoomBtn)

        self.layout.addLayout(self.topL)
        self.layout.addWidget(self.outputBox)
        self.layout.addWidget(self.inputBox)
        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)

        #self.currentRoom = self.rooms.currentText()

        # SET UP THE CLIENT IN A NEW THREAD:
        self.client = Client()
        self.thread = QThread(self)
        self.client.messageSignal.connect(self.receive_info)

        self.client.roomListSignal.connect(self.room_list)

        self.client.errorSignal.connect(self.error_output)
        self.client.greenSignal.connect(self.green_output)
        self.client.joinRoomSignal.connect(self.join_room)
        self.client.delRoomSignal.connect(self.delete_room)

        self.client.moveToThread(self.thread)
        self.thread.started.connect(self.client.run)

        # Connect the buttons/input to client:
        self.inputBox.returnPressed.connect(self.on_press_print)
        self.btn.pressed.connect(self.on_press_print)
        self.rooms.currentIndexChanged.connect(self.change_room)
        self.addRoomBtn.clicked.connect(self.new_room)

        self.roomListBtn.clicked.connect(lambda: self.client.get_room_list())

        # Start the thread!
        self.thread.start()

    # Receive messages from the server and display them to chat.
    @pyqtSlot(str)
    def receive_info(self, msg):
        self.outputBox.append(msg)

    # Receive messages from the server and display them to chat.
    @pyqtSlot(str)
    def green_output(self, msg):
        self.outputBox.append("<span style=\" color:#008000;\" >{}</span>".format(msg))

    @pyqtSlot(str)
    def error_output(self, msg):
        self.outputBox.append("<span style=\" color:#ff0000;\" >{}</span>".format(msg))

    @pyqtSlot(str)
    def get_new_room(self,roomList):
        roomList = roomList.split(' ')
        for i in roomList:
            #if i != "general":
            self.rooms.addItem(i)

    @pyqtSlot(str)
    def join_room(self,room):
        joinedRooms = [self.rooms.itemText(i) for i in range(self.rooms.count())]
        if room not in joinedRooms:
            self.rooms.addItem(room)
        try:
            self.nd.hide()
        except:
            return

    @pyqtSlot(str)
    def delete_room(self,room):
        self.rooms.removeItem(self.rooms.findText(room))
        self.nd.hide()


    @pyqtSlot(str)
    def room_list(self,roomList):

        self.nd = RoomListWindow()
        self.rlayout = QVBoxLayout()
        roomList = roomList.split("\n")[1:]
        #roomList = roomList[1:]
        joinedRooms = [self.rooms.itemText(i) for i in range(self.rooms.count())]

        buttons = []
        for i in roomList:
            tempLayout = QHBoxLayout()
            name = QLabel(self)
            name.setText(i)
            if i in joinedRooms:
                buttons.append(QPushButton("Leave", self.nd))
                buttons[-1].clicked.connect(partial(self.leave_room, data=i))
            else:
                buttons.append(QPushButton("Join", self.nd))
                buttons[-1].clicked.connect(partial(self.select_room, data=i))
            tempLayout.addWidget(name)
            tempLayout.addWidget(buttons[-1])
            self.rlayout.addLayout(tempLayout)
        '''for i in roomList:
            button = QPushButton(i,self.nd)
            button.clicked.connect(lambda: self.select_room(i))
            self.rlayout.addWidget(button)'''
        self.nd.setLayout(self.rlayout)
        self.nd.show()


    def select_room(self, data="\n"):
        self.client.join_room(data)
        print data
        print "i join this room!"
        #self.roomlistwindow.hide()

    def leave_room(self, data="\n"):
        self.client.leave_room(data)
        print "leaving room"




if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("plastique"))
    test = GUIWindow()
    test.show()
    app.exec_()
