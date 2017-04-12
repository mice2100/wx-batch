from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from mainwindow import Ui_MainWindow
from dialogsend_imp import dialogsend_imp
from dialogtoolbox_imp import dialogtoolbox_imp
from wxHelper import *
import zipfile

class mainwindow_imp(Ui_MainWindow, QMainWindow):
    def __init__(self, wxinst, wxhelper):
        super(mainwindow_imp, self).__init__()
#        self.model = QtSql.QSqlTableModel()
        self.jobd = {}
        self.count = 0
        self.wxInst = wxinst
        self.wxHelper = wxhelper
        # self.wxInst = itchat.new_instance()
        # self.wxHelper = wxHelper(self.wxInst)

    def setupUi(self, MainWindow):
        super(mainwindow_imp, self).setupUi(self)
        self.dialogtoolbox_imp = dialogtoolbox_imp(self)
        self.dialogtoolbox_imp.setupUi()
        self.dialogtoolbox_imp.btnSearch.clicked.connect(self.btnSearchClicked)
        self.dialogtoolbox_imp.btnInvalid.clicked.connect(self.btnInvalidClicked)
        self.dialogtoolbox_imp.btnNoremark.clicked.connect(self.btnNoremarkClicked)
        self.dialogtoolbox_imp.btnNotags.clicked.connect(self.btnNotagsClicked)

        self.actionStart.triggered.connect(self.triggerStartWx)
        self.actionStop.triggered.connect(self.triggerStopWx)
        self.actionSend.triggered.connect(self.triggerSend)
        self.actionupdatefromwx.triggered.connect(self.triggerUpdatefromwx)
        self.actionBatchSend.triggered.connect(self.triggerBatchSendStart)
        self.actionStopBatch.triggered.connect(self.triggerBatchSendStop)
        self.actionRemoveSelected.triggered.connect(self.triggerRemoveSelected)
        self.actionQuit.triggered.connect(self.close)
        self.actionBackup.triggered.connect(self.triggerBackup)
        self.dialogtoolbox_imp.show()

        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(self.wxHelper.DBFILE)
        self.model = QtSql.QSqlTableModel()
        self.init_model()
        self.tableView.setModel(self.model)
        self.tableView.hideColumn(1)
        self.tableView.hideColumn(6)
        self.tableView.setSortingEnabled(True)
        while self.model.canFetchMore(): self.model.fetchMore()
        self.count = self.model.rowCount()
        xx = "%d rows in total" % self.count
        self.lbMsg.setText(xx)

    def closeEvent(self, event):
        self.triggerBatchSendStop()
        self.triggerStopWx()
        event.accept()

    def dofilter(self, cond):
        self.model.setFilter(cond)
        self.model.select()
        while self.model.canFetchMore(): self.model.fetchMore()
        self.count = self.model.rowCount()
        xx = "%d rows in total" % self.count
        self.lbMsg.setText(xx)
        # print(cond)
        # Connect up the buttons.
        #    self.btnClose.clicked.connect()
    def btnSearchClicked(self):
        cond = make_cond_from_dict(self.dialogtoolbox_imp.jobd)
        self.dofilter(cond)

    def btnInvalidClicked(self):
        cond = "up2date=0"
        self.dofilter(cond)

    def btnNoremarkClicked(self):
        cond = "alias='' and (remark is NULL or length(remark)=0)"
        self.dofilter(cond)

    def btnNotagsClicked(self):
        cond = "tags is NULL or length(tags)=0"
        self.dofilter(cond)

    def triggerStartWx(self):
        if self.wxInst.alive: return
        self.wxInst.auto_login(hotReload=True)
        self.wxInst.run(blockThread=False)

    def triggerStopWx(self):
        if not self.wxInst.alive: return
        self.wxInst.logout()
        self.wxInst.dump_login_status()

    def triggerBatchSendStart(self):
        self.wxHelper.start_batchsend()

    def triggerBatchSendStop(self):
        self.wxHelper.stop_batchsend()

    def triggerSend(self):

        selected = self.tableView.selectedIndexes()
        xxx = set()
        for i in selected:
            xxx.add(i.row())

        receipts = []

        for i in xxx:
            tmp = {}
            tmp['nickname'] = self.model.record(i).field('nickname').value()
            tmp['alias'] = self.model.record(i).field('alias').value()
            tmp['remark'] = self.model.record(i).field('remark').value()
            tmp['prefix'] = self.model.record(i).field('prefix').value()
            receipts.append(tmp)

        dlg = dialogsend_imp(self)
        dlg.setupUi()
        dlg.lblCount.setText(str(len(xxx)))

        dlg.exec()
        if dlg.result()==QDialog.Accepted:
            # dd = dict(dlg.jobd, **self.dialogtoolbox_imp.jobd)
            dd = dlg.jobd
            dd['receipts'] = receipts
            self.wxHelper.add_send_jobs(dd)

    def triggerUpdatefromwx(self):
        if self.wxInst.alive:
            nn = self.wxHelper.saveContact()
            logging.info("本次新增联系人： %d" % nn)
            self.btnSearchClicked()

    def triggerRemoveSelected(self):
        selected = self.tableView.selectedIndexes()
        for i in selected:
            self.model.removeRow(i.row())
        self.btnSearchClicked()

    def triggerBackup(self):
        fname='backup-' + time.strftime("%Y%m%d%H%M%S") + '.zip'
        # con = sqlite3.connect(self.wxHelper.DBFILE)
        # con.execute("VACUUM;")
        # con.close()
        with zipfile.ZipFile(fname, 'w') as zip:
            zip.write(self.wxHelper.DBFILE)

    def before_update(self, row, record):
        if self.wxInst.alive:
            if record.value('tp') != 0: return
            nickname = record.value('nickname')
            alias = record.value('alias')
            usr = self.wxInst.search_friends(wechatAccount=alias, nickName=nickname)
            if usr is not None and len(usr)>0:
                remark = usr[0]['RemarkName']
                if remark != record.value('remark'):
                    uid = usr[0]['UserName']
                    self.wxInst.set_alias(uid, record.value('remark'))
        # logging.debug(record.value('mobile'))

    def init_model(self):
        self.model.setTable('contacts')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.beforeUpdate.connect(self.before_update)

        headers = ['微信名', '标识', '性别', '省', '市', '微信ID', 'sns', '称呼', '标签', '类型', '微信备注', '更新状态', '手机号', '备注']
        for i in range(len(headers)):
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, headers[i])
        self.model.select()

"""DB related
"""
