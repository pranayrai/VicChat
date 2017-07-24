#Simple proof of concept GUI

import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from time import sleep



class GUI:

    app = QApplication(sys.argv)
    login = QWidget()
    w = QWidget()
    username = ''
    rooms = QComboBox(w)

    commands = []
    outputBox = QPlainTextEdit(w)



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

        #create our window


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




if __name__ == "__main__":
    gui = GUI()
