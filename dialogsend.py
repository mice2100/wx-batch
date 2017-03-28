# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogsend.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialogsend(object):
    def setupUi(self, dialogsend):
        dialogsend.setObjectName("dialogsend")
        dialogsend.resize(435, 238)
        dialogsend.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialogsend)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(dialogsend)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.cbPrefix = QtWidgets.QCheckBox(dialogsend)
        self.cbPrefix.setChecked(True)
        self.cbPrefix.setObjectName("cbPrefix")
        self.horizontalLayout_2.addWidget(self.cbPrefix)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.edtMsg = QtWidgets.QTextEdit(dialogsend)
        self.edtMsg.setObjectName("edtMsg")
        self.verticalLayout_2.addWidget(self.edtMsg)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(dialogsend)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.edtPic = QtWidgets.QLineEdit(dialogsend)
        self.edtPic.setObjectName("edtPic")
        self.horizontalLayout_5.addWidget(self.edtPic)
        self.btnBrowse = QtWidgets.QPushButton(dialogsend)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBrowse.sizePolicy().hasHeightForWidth())
        self.btnBrowse.setSizePolicy(sizePolicy)
        self.btnBrowse.setObjectName("btnBrowse")
        self.horizontalLayout_5.addWidget(self.btnBrowse)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(dialogsend)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 2)
        self.btnSend = QtWidgets.QPushButton(dialogsend)
        self.btnSend.setObjectName("btnSend")
        self.gridLayout_2.addWidget(self.btnSend, 2, 1, 1, 1)
        self.btnCancel = QtWidgets.QPushButton(dialogsend)
        self.btnCancel.setObjectName("btnCancel")
        self.gridLayout_2.addWidget(self.btnCancel, 2, 2, 1, 1)
        self.lblCount = QtWidgets.QLabel(dialogsend)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblCount.setFont(font)
        self.lblCount.setObjectName("lblCount")
        self.gridLayout_2.addWidget(self.lblCount, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(dialogsend)
        QtCore.QMetaObject.connectSlotsByName(dialogsend)
        dialogsend.setTabOrder(self.cbPrefix, self.edtMsg)
        dialogsend.setTabOrder(self.edtMsg, self.edtPic)
        dialogsend.setTabOrder(self.edtPic, self.btnBrowse)

    def retranslateUi(self, dialogsend):
        _translate = QtCore.QCoreApplication.translate
        dialogsend.setWindowTitle(_translate("dialogsend", "批量发送信息"))
        self.label.setText(_translate("dialogsend", "发送文本："))
        self.cbPrefix.setText(_translate("dialogsend", "使用称呼(文本里用%s代替)"))
        self.edtMsg.setHtml(_translate("dialogsend", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%s你好，这是一条测试信息</p></body></html>"))
        self.label_3.setText(_translate("dialogsend", "发送图像："))
        self.btnBrowse.setText(_translate("dialogsend", "..."))
        self.label_2.setText(_translate("dialogsend", "即将接收到信息的好友数量："))
        self.btnSend.setText(_translate("dialogsend", "发送"))
        self.btnCancel.setText(_translate("dialogsend", "取消"))
        self.lblCount.setText(_translate("dialogsend", "120"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialogsend = QtWidgets.QDialog()
    ui = Ui_dialogsend()
    ui.setupUi(dialogsend)
    dialogsend.show()
    sys.exit(app.exec_())

