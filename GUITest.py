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
    def new_room(self):
        text, ok = QInputDialog.getText(self, 'Create new room', 'Enter a room name:')
        if ok:
            self.rooms.addItem(text)
            self.rooms.setCurrentIndex(self.rooms.count()-1)
        #self.commands.append("New room: " + text)

    # This is called when the room selection is changed
    def change_room(self):
        print "Changing room to {}...".format(self.rooms.currentText())
        self.outputBox.clear()
        #self.commands.append("Change room: " + self.rooms.currentText())

    #Prints the message to the message history, and clears the input box
    @pyqtSlot()
    def on_press_print(self):
        message = self.inputBox.text()
        #outputBox.appendPlainText("(time) You: " + message)
        self.inputBox.clear()
        #self.commands.append("New message: " + message)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

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
        self.rooms.addItem("General")
        self.rooms.addItem("Random")

        # Button to add a new room
        self.addRoomBtn = QPushButton('New Room', self)
        self.addRoomBtn.setToolTip('Click to create a new room')
        self.addRoomBtn.clicked.connect(self.new_room)

        #Place everything on the screen
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

        # connect the signals to the slots


        self.rooms.currentIndexChanged.connect(self.change_room)


        self.client = Client()
        self.thread = QThread(self)
        self.client.messageSignal.connect(self.receive_info)
        self.client.errorSignal.connect(self.connection_error)
        self.client.moveToThread(self.thread)
        self.thread.started.connect(self.client.run)

        self.inputBox.returnPressed.connect(lambda: self.client.send_message(self.inputBox.text()))
        self.inputBox.returnPressed.connect(self.on_press_print)
        self.btn.pressed.connect(lambda: self.client.send_message(self.inputBox.text()))
        self.btn.pressed.connect(self.on_press_print)
        #self.inputBox.returnPressed.connect(self.client.send_message(self.inputBox.text()))
        self.thread.start()

    @pyqtSlot(str)
    def receive_info(self, msg):
        self.outputBox.appendPlainText(msg)

    @pyqtSlot(str)
    def connection_error(self):
        self.outputBox.appendPlainText("Could not connect to server.")




# --- EVERYTHING BELOW THIS LINE IS OLD AND NOT USED ---



class GUI:

    app = QApplication(sys.argv)
    login = QWidget()
    w = QWidget()
    username = ''
    rooms = QComboBox(w)

    commands = []
    outputBox = QPlainTextEdit(w)

    #client = client()




    def __init__(self):

        # This is called when the new room button is pressed
        def new_room():
            text, ok = QInputDialog.getText(self.w, 'Create new room', 'Enter a room name:')
            if ok:
                self.rooms.addItem(text)
                self.rooms.setCurrentIndex(self.rooms.count()-1)
            self.commands.append("New room: " + text)

        # This is called when the room selection is changed
        def change_room():
            print "Changing room to {}...".format(self.rooms.currentText())
            self.outputBox.clear()
            self.commands.append("Change room: " + self.rooms.currentText())



        #           Create the actions:
        #
        #Prints the message to the message history, and clears the input box
        @pyqtSlot()
        def on_press_print():
            message = inputBox.text()
            #outputBox.appendPlainText("(time) You: " + message)
            inputBox.clear()
            self.commands.append("New message: " + message)

        #Creates a popup to confirm if the user wants to exit the program
        @pyqtSlot()
        def on_press_exit():
            ans = QMessageBox.question(w, 'Message', "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ans == QMessageBox.Yes:
                exit(0)
            else:
                pass

        def change_windows():
            self.login.hide()
            self.app.setStyle(QStyleFactory.create(themeList.currentText()))
            self.username = nameInput.text()
            self.w.show()




        # Select the theme
        #app.setStyle(QStyleFactory.create("cde"))


        loginLayout = QVBoxLayout()
        nameLabel = QLabel(self.login)
        nameLabel.setText("Enter a Username:")
        loginLayout.addWidget(nameLabel)
        nameInput = QLineEdit(self.login)
        nameInput.setPlaceholderText("enter name here")
        loginLayout.addWidget(nameInput)
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
        loginButton.pressed.connect(change_windows)
        nameInput.returnPressed.connect(change_windows)



        self.w.setWindowTitle('VicChat GUI prototype')
        self.w.resize(320,310)

        # Create the output button
        btn = QPushButton('Print text to console', self.w)

        # Create textbox for data-entry
        inputBox = QLineEdit(self.w)
        inputBox.setPlaceholderText("enter message here")

        # Create a multi-line textbox to display history
        #outputBox = QPlainTextEdit(self.w)
        self.outputBox.setReadOnly(True)
        self.outputBox.appendPlainText("""(12:52) Matt: Did anyone get that new chat room button?
        (12:55) Bryan: I think the tabs function broke it
        (12:58) Matt: Didn't Bob fix that?
        (12:59) Bryan: Yeah, but it broke formatting on everything, so we didn't push it
        (1:01) Matt: Gotcha
        (1:02) Matt: Eta on that Bob?
        (1:15) Bob: Working on it, give me a couple hours
        (1:18) Matt: Roger""")

        # Add the room label
        roomLabel = QLabel(self.w)
        roomLabel.setText("Room: ")

        # Create combobox for room list
        #rooms = QComboBox(self.w)
        self.rooms.addItem("General")
        self.rooms.addItem("Random")

        # Button to add a new room
        addRoomBtn = QPushButton('New Room', self.w)
        addRoomBtn.setToolTip('Click to create a new room')
        addRoomBtn.clicked.connect(new_room)

        #Place everything on the screen
        layout = QVBoxLayout()
        topL = QHBoxLayout()
        topL.addWidget(roomLabel)
        topL.addWidget(self.rooms)
        topL.addStretch()
        topL.addWidget(addRoomBtn)

        layout.addLayout(topL)
        layout.addWidget(self.outputBox)
        layout.addWidget(inputBox)
        layout.addWidget(btn)


        self.w.setLayout(layout)

        # connect the signals to the slots
        btn.pressed.connect(on_press_print)
        inputBox.returnPressed.connect(on_press_print)
        self.rooms.currentIndexChanged.connect(change_room)


        # This locks all keyboard input in the app to this box
        # Not a good solution
        # inputBox.grabKeyboard()

        # Show the window and run the app
        #w.show()
        self.app.exec_()


    def gui_input():
        commandList = self.commands
        self.commands = []
        return commandList

    def gui_output(newRooms,chat):
        if newRooms is not None:
            for i in newRooms:
                self.rooms.addItem(text)
        if chat is not None:
            for i in chat:
                self.outputBox.appendPlainText(i)

    def no_connection():
        box = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Could not connect to server")
        msg.buttonClicked.connect(exit(0))


if __name__ == "__main__":
    #gui = GUI()

    app = QApplication(sys.argv)
    test = GUIWindow()
    test.show()
    app.exec_()
