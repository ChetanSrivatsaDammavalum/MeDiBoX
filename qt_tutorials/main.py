# Version 1
"""

from PySide6.QtWidgets import QApplication , QMainWindow, QPushButton

# module for processing command line arguments
import sys

# wrapper to run the application and interaction(I/O) with the application
app = QApplication(sys.argv)

# by default, window or widgets are hidden
window = QMainWindow()
window.setWindowTitle("MeDiBoX")

button = QPushButton()
button.setText("Login")

window.setCentralWidget(button)

window.show()

# exec method to start the application event loop -> a while loop waiting for events to happen
app.exec() 

"""

# Version 2
"""

from PySide6.QtWidgets import QApplication , QMainWindow, QPushButton

# module for processing command line arguments
import sys


class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Holder app")
        button = QPushButton(" Login ")

        #Set up the button as central widget
        self.setCentralWidget(button)

# wrapper to run the application and interaction(I/O) with the application
app = QApplication(sys.argv)

# by default, window or widgets are hidden
window = ButtonHolder()
window.show()

# exec method to start the application event loop -> a while loop waiting for events to happen
app.exec() 

"""
# Version 3
"""
from PySide6.QtWidgets import QApplication 
from button_holder import ButtonHolder # custom class

# module for processing command line arguments
import sys

app = QApplication(sys.argv)

# by default, window or widgets are hidden
window = ButtonHolder()
window.show()

# exec method to start the application event loop -> a while loop waiting for events to happen
app.exec() 

"""
# Signals and slots
# Verison 1
"""

from PySide6.QtWidgets import QApplication, QPushButton 

# the slot: responds when something happens
def button_clicked():
    print("You clicked the button")

app = QApplication()
button = QPushButton("press Me")

# clicked is signal of QPushButton. It's emitted when you click
# on the button
# You can wire a slot to the signal using the syntax below:
button.clicked.connect(button_clicked)
button.show()

# exec method to start the application event loop -> a while loop waiting for events to happen
app.exec() 

"""
# Version 2
# signals sending values, capture values in slots

"""
from PySide6.QtWidgets import QApplication, QPushButton 

# the slot: responds when something happens
def button_clicked(data): # <- signal sending value 
    print("You clicked the button !, Checked:",data)

app = QApplication()
button = QPushButton("press Me")
button.setCheckable(True) # Makes the button checkable. Its's uncheckd by default
                          # Further clicks toggles between checked and unchecked

# clicked is signal of QPushButton. It's emitted when you click
# on the button
# You can wire a slot to the signal using the syntax below:
button.clicked.connect(button_clicked)
button.show()

# exec method to start the application event loop -> a while loop waiting for events to happen
app.exec() 

"""
# Version 3
# Capture the value of slider 
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSlider 

# the slot: responds when something happens
def respond_to_slider(data):
    print("slider moved to :", data)

app = QApplication()
slider = QSlider(Qt.Horizontal)
slider.setMinimum(1)
slider.setMaximum(100)
slider.setValue(25)

# You just do the connection. The Qt syste takes care of
# passing the data from the signal to the slot.
slider.valueChanged.connect(respond_to_slider)
slider.show()
app.exec()

"""

# Qt Widgets -> Widgets are basic units of UI 
# eg., QpushButton, QLineEdit, QTextEdit, QMainWindow, Layouts, Size Policies and Stretches, etc.

# Layout
"""
from PySide6.QtWidgets import QApplication
from rockwidget import RockWidget # custom class
import sys

app = QApplication(sys.argv)

window = RockWidget() 
window.show()

app.exec()

"""

# QMainWindow -> Allows us to work with Menus, Toolbars, Status bars, Actions etc.
""""""
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow # custom class
import sys

app = QApplication(sys.argv)

window = MainWindow(app) 
window.show()

app.exec()

""""""