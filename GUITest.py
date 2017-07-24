#Simple proof of concept GUI

import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from time import sleep


# This is called when the new room button is pressed
def new_room():
    text, ok = QInputDialog.getText(w, 'Create new room', 'Enter a room name:')
    if ok:
        rooms.addItem(text)
        rooms.setCurrentIndex(rooms.count()-1)

# This is called when the room selection is changed
def change_room():
    print "Changing room to {}...".format(rooms.currentText())
    outputBox.clear()

def change_windows():
    login.hide()
    app.setStyle(QStyleFactory.create(themeList.currentText()))
    username = nameInput.text()
    w.show()

#create our window
app = QApplication(sys.argv)

# Select the theme
#app.setStyle(QStyleFactory.create("cde"))

login = QWidget()
loginLayout = QVBoxLayout()
nameLabel = QLabel(login)
nameLabel.setText("Enter a Username:")
loginLayout.addWidget(nameLabel)
nameInput = QLineEdit(login)
nameInput.setPlaceholderText("enter name here")
loginLayout.addWidget(nameInput)
themeLabel = QLabel(login)
themeLabel.setText("Choose a theme:")
loginLayout.addWidget(themeLabel)
themeList = QComboBox(login)
themeList.addItems(QStyleFactory.keys())
loginLayout.addWidget(themeList)
# find current style
index = themeList.findText(
            qApp.style().objectName(),
            Qt.MatchFixedString)
# set current style
themeList.setCurrentIndex(index)
loginButton = QPushButton('Login', login)
loginLayout.addWidget(loginButton)
login.setLayout(loginLayout)

login.show()
loginButton.pressed.connect(change_windows)

username = ''



w = QWidget()
w.setWindowTitle('VicChat GUI prototype')
w.resize(320,310)

# Create the output button
btn = QPushButton('Print text to console', w)

# Create textbox for data-entry
inputBox = QLineEdit(w)
inputBox.setPlaceholderText("enter message here")

# Create a multi-line textbox to display history
outputBox = QPlainTextEdit(w)
outputBox.setReadOnly(True)
outputBox.appendPlainText("""(12:52) Matt: Did anyone get that new chat room button?
(12:55) Bryan: I think the tabs function broke it
(12:58) Matt: Didn't Bob fix that?
(12:59) Bryan: Yeah, but it broke formatting on everything, so we didn't push it
(1:01) Matt: Gotcha
(1:02) Matt: Eta on that Bob?
(1:15) Bob: Working on it, give me a couple hours
(1:18) Matt: Roger""")

# Add the room label
roomLabel = QLabel(w)
roomLabel.setText("Room: ")

# Create combobox for room list
rooms = QComboBox(w)
rooms.addItem("General")
rooms.addItem("Random")
rooms.addItem("room3")
rooms.addItem("room4")

# Button to add a new room
addRoomBtn = QPushButton('New Room', w)
addRoomBtn.setToolTip('Click to create a new room')
addRoomBtn.clicked.connect(new_room)

#Place everything on the screen
layout = QVBoxLayout()
topL = QHBoxLayout()
topL.addWidget(roomLabel)
topL.addWidget(rooms)
topL.addStretch()
topL.addWidget(addRoomBtn)

layout.addLayout(topL)
layout.addWidget(outputBox)
layout.addWidget(inputBox)
layout.addWidget(btn)


w.setLayout(layout)





#           Create the actions:
#
#Prints the message to the message history, and clears the input box
@pyqtSlot()
def on_press_print():
    message = inputBox.text()
    outputBox.appendPlainText("(time) You: " + message)
    inputBox.clear()


#Creates a popup to confirm if the user wants to exit the program
@pyqtSlot()
def on_press_exit():
    ans = QMessageBox.question(w, 'Message', "Are you sure you want to quit?",
                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if ans == QMessageBox.Yes:
        exit(0)
    else:
        pass


# connect the signals to the slots
btn.pressed.connect(on_press_print)
inputBox.returnPressed.connect(on_press_print)
rooms.currentIndexChanged.connect(change_room)


# This locks all keyboard input in the app to this box
# Not a good solution
# inputBox.grabKeyboard()

# Show the window and run the app
#w.show()
app.exec_()
