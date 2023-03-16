from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout

# QWidget class inherited by parent widget(RockWidget)
# Adding push button in the RockWidget will not result in showing button in the widget as 
# the widget doesn't have information on where to place the button. 
# To add elements in RockWidget, Layout has to be set -> QHBoxlayout in this case.

class RockWidget(QWidget): # inherits from QWidget class
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RockWidget")
        button1 = QPushButton("Button 1")
        button1.clicked.connect(self.button1_clicked)

        button2 = QPushButton("Button 2")
        button2.clicked.connect(self.button2_clicked)
        
        button3 = QPushButton("Button 3")
        button3.clicked.connect(self.button3_clicked)
        
        button4 = QPushButton("Button 4")
        button4.clicked.connect(self.button4_clicked)


        button_layout_1 = QHBoxLayout()
        button_layout_1.addWidget(button1)
        button_layout_1.addWidget(button2)

        button_layout_2 = QVBoxLayout()
        button_layout_2.addWidget(button3)
        button_layout_2.addWidget(button4)

        # method to let the widget use the layout component to lay the elements inside the widget
        #self.setLayout(button_layout_1)
        self.setLayout(button_layout_2)

    def button1_clicked(self):
        print("Button1 clicked")

    def button2_clicked(self):
        print("Button2 clicked")

    def button3_clicked(self):
        print("Button3 clicked")

    def button4_clicked(self):
        print("Button4 clicked")