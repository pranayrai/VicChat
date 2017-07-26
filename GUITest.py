#Simple proof of concept GUI

import sys
import threading
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from time import sleep
from Client import Client



class GUIWindow(QWidget):
    # This is called when the new room button is pressed
    @pyqtSlot()
    def new_room(self):
        text, ok = QInputDialog.getText(self, 'Create new room', 'Enter a room name:')
        if ok:
            self.rooms.addItem(text)
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
        self.client.join_room(self.rooms.currentText())
        self.outputBox.clear()
        self.currentRoom = self.rooms.currentText()

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
        self.outputBox = QPlainTextEdit(self)
        self.outputBox.setReadOnly(True)

        # Add the room label
        self.roomLabel = QLabel(self)
        self.roomLabel.setText("Room: ")

        # Create combobox for room list
        self.rooms = QComboBox(self)
        self.rooms.addItem("general")
        #self.rooms.addItem("Random")

        # Button to add a new room
        self.addRoomBtn = QPushButton('New Room', self)
        self.addRoomBtn.setToolTip('Click to create a new room')

        #Place everything on the screen using a layout
        self.layout = QVBoxLayout()
        self.topL = QHBoxLayout()
        self.topL.addWidget(self.roomLabel)
        self.topL.addWidget(self.rooms)
        self.topL.addStretch()
        self.topL.addWidget(self.addRoomBtn)

        self.layout.addLayout(self.topL)
        self.layout.addWidget(self.outputBox)
        self.layout.addWidget(self.inputBox)
        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)

        self.currentRoom = self.rooms.currentText()

        # SET UP THE CLIENT IN A NEW THREAD:
        self.client = Client()
        self.thread = QThread(self)
        self.client.messageSignal.connect(self.receive_info)
        self.client.roomListSignal.connect(self.get_new_room)
        self.client.errorSignal.connect(self.connection_error)
        self.client.moveToThread(self.thread)
        self.thread.started.connect(self.client.run)

        # Connect the buttons/input to client:
        self.inputBox.returnPressed.connect(self.on_press_print)
        self.btn.pressed.connect(self.on_press_print)
        self.rooms.currentIndexChanged.connect(self.change_room)
        self.addRoomBtn.clicked.connect(self.new_room)

        # Start the thread!
        self.thread.start()

    # Receive messages from the server and display them to chat.
    @pyqtSlot(str)
    def receive_info(self, msg):
        self.outputBox.appendPlainText(msg)

    # Error when you cannot connect to chat.
    @pyqtSlot()
    def connection_error(self):
        self.outputBox.appendPlainText("Could not connect to server.")

    @pyqtSlot(str)
    def get_new_room(self,rooms):
        for i in rooms.split():
            self.rooms.addItem(i)


    @pyqtSlot()
    def room_list(self,roomList):

        self.roomlistwindow = QWidget()
        rlayout = QVBoxLayout()

        buttons = []
        for i in roomList.items():
            buttons.append(QPushButton(i, self.roomlistwindow))
            buttons[-1].clicked.connect(partial(self.select_room, data=i))
            rlayout.addWidget(buttons[-1])
        self.roomlistwindow.setLayout(self.layout)


    def select_room(self, data="\n"):
        print data
        print "i join this room!"




if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("plastique"))
    test = GUIWindow()
    test.show()
    app.exec_()
