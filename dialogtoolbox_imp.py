from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from dialogtoolbox import Ui_dialogtoolbox
import logging
import json


class MyLogHandler(logging.Handler):

    def __init__(self, parent):
        logging.Handler.__init__(self)
        self.jobd={}
        self.parent = parent

    def emit(self, record):
        self.parent.write(self.format(record))

class dialogtoolbox_imp(Ui_dialogtoolbox, QDialog):
    def __init__(self, parent):
        super(dialogtoolbox_imp, self).__init__()
        self.setParent(parent)
        self.jobd = {}

    def browseFile(self):
        fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt)")
        if len(fileName)>0:
            self.edtPic.setText(fileName)

    def write(self, s):
        self.txtLog.append(s)
        sb = self.txtLog.verticalScrollBar()
        sb.setValue(sb.maximum())

    def make_cond(self):
        self.jobd['province'] = self.edtProv.text()
        self.jobd['city'] = self.edtCity.text()
        self.jobd['sex'] = self.edtSex.text()
        self.jobd['remark'] = self.edtRemark.text()
        self.jobd['type'] = self.edtType.text()
        self.jobd['name'] = self.edtName.text()
        self.jobd['tags'] = self.edtTags.text()

    def setupUi(self):
        super(dialogtoolbox_imp, self).setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)
        # loghandler = MyLogHandler(self)
        # loghandler.setFormatter(logging.Formatter('%(levelname)s: %(filename)s - %(message)s'))
        # loghandler.setFormatter(logging.Formatter('%(message)s'))
        # logging.getLogger().addHandler(loghandler)
        # logging.getLogger().setLevel(logging.DEBUG)

        self.btnSearch.clicked.connect(self.make_cond)


