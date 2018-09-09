from views.mainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow


class mainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
