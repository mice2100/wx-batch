from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog
from dialogsend import Ui_dialogsend

class dialogsend_imp(QDialog, Ui_dialogsend):
    def __init__(self, parent=None):
        super(dialogsend_imp, self).__init__(parent)
        self.jobd = {}

    def browseFile(self,ctl):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt)")
        if len(fileName)>0:
            ctl.setText(fileName)

    def make_cond(self):
        self.jobd['msg'] = self.edtMsg.toPlainText()
        self.jobd['prefix'] = self.cbPrefix.checkState()
        self.jobd['pic'] = self.edtPic.text()
        self.jobd['pic_2'] = self.edtPic_3.text()
        self.jobd['pic_3'] = self.edtPic_4.text()

    def btnSendClicked(self):
        self.make_cond()
        self.accept()

    def setupUi(self):
        super(dialogsend_imp, self).setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)
        self.btnBrowse.clicked.connect(lambda: self.browseFile(self.edtPic))
        self.btnBrowse_3.clicked.connect(lambda: self.browseFile(self.edtPic_3))
        self.btnBrowse_4.clicked.connect(lambda: self.browseFile(self.edtPic_4))
        self.btnSend.clicked.connect(self.btnSendClicked)
        self.btnCancel.clicked.connect(self.reject)

