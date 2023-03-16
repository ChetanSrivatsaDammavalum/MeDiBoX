from PySide6.QtCore import QSize 
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow,QToolBar

# custom class mainWindow inherits from QMainWindow 
class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app # declare an application member which creats the mainWindow
                       # This member will be used to quit the mainWindow
        self.setWindowTitle("Custom MainWindow")
        
        # Members and Menus
        menu_bar = self.menuBar() # method in QMainWindow called by MainWindow object to create menus
        file_menu = menu_bar.addMenu("File") # method to add a menu to the menu bar
        quit_action = file_menu.addAction("Quit") # add menu actions to the file_menu -> here action is named Quit
                                                  # assign a variable to record the trigger of the action
        quit_action.triggered.connect(self.quit_app) # from signal and slot 
        
        edit_menu = menu_bar.addMenu("&Edit")# & -> resuts in underline on following single string element
        edit_menu.addAction("Copy")
        edit_menu.addAction("Cut")
        edit_menu.addAction("Paste")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        menu_bar.addMenu("Window")
        menu_bar.addMenu("settings")
        menu_bar.addMenu("Help")

        # Toolbars 
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        toolbar.addAction(quit_action)# add action to the toolbar
                                      # essentially we can terminate the QMainWindow from both the file_menu and tool bar

        # custom action
        action_1 = QAction("Some Action", self)
        action_1.setStatusTip("Status message for some action")
        action_1.triggered.connect(self.toolbar_button_click)
        toolbar.addAction(action_1)



    def quit_app(self): # method in class takes self as first argument
        self.app.quit()                        
    
    def toolbar_button_click(self):
        print("action triggered")