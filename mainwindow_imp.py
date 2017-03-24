from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog
from mainwindow import Ui_MainWindow
from dialogsend_imp import dialogsend_imp
from newWxBot import *

def initializeModel(model):
    model.setTable('contacts')
    model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
    model.select()
    """
    model.setHeaderData(0, QtCore.Qt.Horizontal, "NickName")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Alias")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Prefix")
    """

class mainwindow_imp(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(mainwindow_imp, self).__init__()
#        self.model = QtSql.QSqlTableModel()
        self.jobd = {}

    def setupUi(self, MainWindow):
        super(mainwindow_imp, self).setupUi(MainWindow)
        tt = QtWidgets.QDialog(MainWindow)
        self.dialogsend_imp = dialogsend_imp()
        self.dialogsend_imp.setupUi(tt)
        self.dialogsend_imp.btnSearch.clicked.connect(self.search)
        self.dialogsend_imp.btnUpdateContacts.clicked.connect(self.search)
        # self.options_imp.btnSearch.clicked.connect(self.search)
        # self.btnBatchSend.clicked.connect(self.sendclicked)
        # self.options_imp.show()
        tt.show()

        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('wechat.db')
        self.model = QtSql.QSqlTableModel()
        initializeModel(self.model)
        self.tableView.setModel(self.model)
        while self.model.canFetchMore(): self.model.fetchMore()
        xx = "%d rows in total" % self.model.rowCount()
        self.lbMsg.setText(xx)

    def sendclicked(self):
        tt = QtWidgets.QDialog()
        uu = dialogsend_imp()
        uu.setupUi(tt)
        tt.setModal(True)
        tt.exec_()

    def search(self):
        cond = make_cond_from_json(JOBFILE)
        # logging.info(cond)
        self.model.setFilter(cond)
        while self.model.canFetchMore(): self.model.fetchMore()
        xx = "%d rows in total" % self.model.rowCount()
        self.lbMsg.setText(xx)
        #print(cond)
        # Connect up the buttons.
    #    self.btnClose.clicked.connect()