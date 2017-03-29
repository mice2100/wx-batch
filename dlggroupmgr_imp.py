from PyQt5 import QtSql, QtCore
from PyQt5.QtWidgets import QDialog
from dlggroupmgr import Ui_dlggroupmgr
import logging, time

class dlggroupmgr_imp(QDialog, Ui_dlggroupmgr):
    def __init__(self, parent=None):
        super(dlggroupmgr_imp, self).__init__(parent)
        # db = QtSql.QSqlDatabase.addDatabase('QSQLITE', 'memory')
        # db.setDatabaseName(':memory:')
        self.model_friend = QtSql.QSqlTableModel()
        self.model_unknown = QtSql.QSqlTableModel()
        self.cnt_friend = 0
        self.cnt_unknown = 0
        self.groupname = ""
        self.wxInst = None
        self.wxHelper = None

    def setupUi(self):
        super(dlggroupmgr_imp, self).setupUi(self)
        self.lblGroupName.setText(self.groupname)
        self.lblFriendCnt.setText(str(self.cnt_friend))
        self.lblUnknowCnt.setText(str(self.cnt_unknown))
        self.lblTotalCnt.setText(str(self.cnt_friend+self.cnt_unknown))
        self.edtHello.setText('您好，我从群聊%s中加您的'%self.groupname)
        self.model_friend.setTable('groupmember')
        self.model_friend.setFilter('isfriend=1')
        self.model_unknown.setTable('groupmember')
        self.model_unknown.setFilter('isfriend=0')

        try:
            headers = ['微信ID', '名字']
            for i in range(len(headers)):
                self.model_friend.setHeaderData(i, QtCore.Qt.Horizontal, headers[i])
                self.model_unknown.setHeaderData(i, QtCore.Qt.Horizontal, headers[i])
            self.model_friend.select()
            self.model_unknown.select()

            self.twFriends.setModel(self.model_friend)
            self.twFriends.hideColumn(0)
            self.twFriends.hideColumn(2)
            self.twFriends.setColumnWidth(1, 200)
            self.twUnknown.setModel(self.model_unknown)
            self.twUnknown.hideColumn(0)
            self.twUnknown.hideColumn(2)
            self.twUnknown.setColumnWidth(1, 200)
        except Exception as e:
            print(e)

        self.btnAddFriends.clicked.connect(self.addFriends)
        self.btnTags.clicked.connect(self.tagFriends)

    def addFriends(self):
        selected = self.twUnknown.selectedIndexes()
        for cur in selected:
            uname = self.model_unknown.record(cur.row()).field('UserName').value()
            logging.debug("Adding friend: %s" % uname)
            if self.wxInst is not None:
                self.wxInst.add_friend(uname, verifyContent=self.edtHello.text())
            time.sleep(2)

    def tagFriends(self):
        fri = []
        if len(self.edtTag.text())<=0: return
        for i in range(self.model_friend.rowCount()):
            rec = self.model_friend.record(i)
            username = rec.field('UserName').value()
            fri.append(username)
        self.wxHelper.tag_usernames(fri, self.edtTag.text())
