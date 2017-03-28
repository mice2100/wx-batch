# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 1, 1, 5)
        self.lbMsg = QtWidgets.QLabel(self.centralwidget)
        self.lbMsg.setObjectName("lbMsg")
        self.gridLayout.addWidget(self.lbMsg, 2, 1, 1, 4)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1280, 23))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menuBar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menuBar)
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtWidgets.QAction(MainWindow)
        self.actionStop.setObjectName("actionStop")
        self.actionBatchSend = QtWidgets.QAction(MainWindow)
        self.actionBatchSend.setObjectName("actionBatchSend")
        self.actionStopBatch = QtWidgets.QAction(MainWindow)
        self.actionStopBatch.setObjectName("actionStopBatch")
        self.actionQUIT = QtWidgets.QAction(MainWindow)
        self.actionQUIT.setObjectName("actionQUIT")
        self.actionSend = QtWidgets.QAction(MainWindow)
        self.actionSend.setObjectName("actionSend")
        self.actionupdatefromwx = QtWidgets.QAction(MainWindow)
        self.actionupdatefromwx.setObjectName("actionupdatefromwx")
        self.actionRemoveSelected = QtWidgets.QAction(MainWindow)
        self.actionRemoveSelected.setObjectName("actionRemoveSelected")
        self.toolBar.addAction(self.actionSend)
        self.toolBar.addSeparator()
        self.menu.addAction(self.actionStart)
        self.menu.addAction(self.actionStop)
        self.menu.addSeparator()
        self.menu.addAction(self.actionBatchSend)
        self.menu.addAction(self.actionStopBatch)
        self.menu.addSeparator()
        self.menu.addAction(self.actionSend)
        self.menu.addSeparator()
        self.menu.addAction(self.actionQUIT)
        self.menu_2.addAction(self.actionQUIT)
        self.menu_3.addAction(self.actionupdatefromwx)
        self.menu_3.addAction(self.actionRemoveSelected)
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "N8微信通讯录管理"))
        self.lbMsg.setText(_translate("MainWindow", "TextLabel"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.menu.setTitle(_translate("MainWindow", "微信操作"))
        self.menu_2.setTitle(_translate("MainWindow", "文件"))
        self.menu_3.setTitle(_translate("MainWindow", "通讯录操作"))
        self.actionStart.setText(_translate("MainWindow", "启动微信"))
        self.actionStart.setIconText(_translate("MainWindow", "启动微信"))
        self.actionStop.setText(_translate("MainWindow", "停止微信"))
        self.actionBatchSend.setText(_translate("MainWindow", "启动批量发送"))
        self.actionStopBatch.setText(_translate("MainWindow", "停止批量发送"))
        self.actionQUIT.setText(_translate("MainWindow", "退出系统"))
        self.actionSend.setText(_translate("MainWindow", "发送消息"))
        self.actionupdatefromwx.setText(_translate("MainWindow", "从微信更新"))
        self.actionRemoveSelected.setText(_translate("MainWindow", "删除选中项"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

