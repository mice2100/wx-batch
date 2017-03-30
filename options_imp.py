from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog
from mainwindow import Ui_MainWindow
from options import Ui_dlgOption


class options_imp(Ui_dlgOption, QDialog):
    def __init__(self):
        super(options_imp, self).__init__()
        self.jobd = {}

    def test(self):
        print("Just a test")

    def setupUi(self, dlgOption):
        super(options_imp, self).setupUi(dlgOption)
        self.btnSearch.clicked.connect(self.test)
        dlgOption.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)

