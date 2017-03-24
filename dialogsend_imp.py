from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog
from mainwindow import Ui_MainWindow
from dialogsend import Ui_dialogsend
from newWxBot import *


class MyLogHandler(logging.Handler):

    def __init__(self, parent):
        logging.Handler.__init__(self)
        self.parent = parent

    def emit(self, record):
        self.parent.write(self.format(record))

class dialogsend_imp(Ui_dialogsend, QDialog):
    def __init__(self):
        super(dialogsend_imp, self).__init__()
        self.jobd = {}
        self.wx = newWxBot()
        self.running = False
        self.sending = False

    def browseFile(self):
        fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt)")
        if len(fileName)>0:
            self.edtPic.setText(fileName)

    def close(self):
        if self.running:
            self.start_wx()
        super(dialogsend_imp,self).close()

    def write(self, s):
        self.txtLog.append(s)
        sb = self.txtLog.verticalScrollBar()
        sb.setValue(sb.maximum())

    def start_wx(self):
        if self.running:
            self.wx.stop()
            self.btnStartWechat.setText("启动微信")
        else:
            self.wx.start()
            self.btnStartWechat.setText("停止微信")
        self.running = not self.running
        self.btnStartSend.setEnabled(self.running)
        self.btnUpdateContacts.setEnabled(self.running)

    def make_cond(self):
        self.jobd['msg'] = self.edtMsg.toPlainText()
        self.jobd['prefix'] = self.cbPrefix.checkState()
        self.jobd['pic'] = self.edtPic.text()
        self.jobd['province'] = self.edtProv.text()
        self.jobd['city'] = self.edtCity.text()
        self.jobd['sex'] = self.edtRemark.text()
        self.jobd['remark'] = self.edtRemark.text()
        self.jobd['type'] = self.edtType.text()
        self.jobd['name'] = self.edtName.text()
        self.jobd['tags'] = self.edtTags.text()


        with open(JOBFILE, 'w') as f:
            f.write(json.dumps(self.jobd, ensure_ascii=False))

    def updateContacts(self):
        if not self.running:
            return

        self.wx.saveContact()

    def start_send(self):
        if self.sending:
            self.wx.stop_batchsend()
            self.btnStartSend.setText("开始发送")
        else:
            self.wx.start_batchsend()
            self.btnStartSend.setText("停止发送")
        self.sending = not self.sending

    def setupUi(self, dlgOption):
        super(dialogsend_imp, self).setupUi(dlgOption)
        dlgOption.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)
        loghandler = MyLogHandler(self)
        # loghandler.setFormatter(logging.Formatter('%(levelname)s: %(filename)s - %(message)s'))
        loghandler.setFormatter(logging.Formatter('%(message)s'))
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger().addHandler(loghandler)
        logging.getLogger().setLevel(logging.DEBUG)

        self.btnBrowse.clicked.connect(self.browseFile)
        self.btnStartSend.clicked.connect(self.start_send)
        self.btnStartWechat.clicked.connect(self.start_wx)
        self.btnUpdateContacts.clicked.connect(self.updateContacts)
        self.btnSearch.clicked.connect(self.make_cond)


