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
        dialogsend.resize(545, 356)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialogsend)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(dialogsend)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.edtTags = QtWidgets.QLineEdit(dialogsend)
        self.edtTags.setObjectName("edtTags")
        self.gridLayout.addWidget(self.edtTags, 5, 1, 1, 1)
        self.edtRemark = QtWidgets.QLineEdit(dialogsend)
        self.edtRemark.setObjectName("edtRemark")
        self.gridLayout.addWidget(self.edtRemark, 2, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(dialogsend)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.edtSex = QtWidgets.QLineEdit(dialogsend)
        self.edtSex.setObjectName("edtSex")
        self.gridLayout.addWidget(self.edtSex, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(dialogsend)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(dialogsend)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(dialogsend)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.edtProv = QtWidgets.QLineEdit(dialogsend)
        self.edtProv.setObjectName("edtProv")
        self.gridLayout.addWidget(self.edtProv, 1, 1, 1, 1)
        self.btnSearch = QtWidgets.QPushButton(dialogsend)
        self.btnSearch.setObjectName("btnSearch")
        self.gridLayout.addWidget(self.btnSearch, 5, 2, 1, 2)
        self.edtCity = QtWidgets.QLineEdit(dialogsend)
        self.edtCity.setObjectName("edtCity")
        self.gridLayout.addWidget(self.edtCity, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(dialogsend)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.edtType = QtWidgets.QLineEdit(dialogsend)
        self.edtType.setObjectName("edtType")
        self.gridLayout.addWidget(self.edtType, 4, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(dialogsend)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 4, 2, 1, 1)
        self.edtName = QtWidgets.QLineEdit(dialogsend)
        self.edtName.setObjectName("edtName")
        self.gridLayout.addWidget(self.edtName, 4, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
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
        self.btnStartWechat = QtWidgets.QPushButton(dialogsend)
        self.btnStartWechat.setObjectName("btnStartWechat")
        self.gridLayout_2.addWidget(self.btnStartWechat, 0, 2, 2, 1)
        self.txtLog = QtWidgets.QTextBrowser(dialogsend)
        self.txtLog.setObjectName("txtLog")
        self.gridLayout_2.addWidget(self.txtLog, 0, 1, 4, 1)
        self.btnStartSend = QtWidgets.QPushButton(dialogsend)
        self.btnStartSend.setEnabled(False)
        self.btnStartSend.setObjectName("btnStartSend")
        self.gridLayout_2.addWidget(self.btnStartSend, 3, 2, 1, 1)
        self.btnUpdateContacts = QtWidgets.QPushButton(dialogsend)
        self.btnUpdateContacts.setEnabled(False)
        self.btnUpdateContacts.setObjectName("btnUpdateContacts")
        self.gridLayout_2.addWidget(self.btnUpdateContacts, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(dialogsend)
        QtCore.QMetaObject.connectSlotsByName(dialogsend)
        dialogsend.setTabOrder(self.edtProv, self.edtCity)
        dialogsend.setTabOrder(self.edtCity, self.edtSex)
        dialogsend.setTabOrder(self.edtSex, self.edtRemark)
        dialogsend.setTabOrder(self.edtRemark, self.edtType)
        dialogsend.setTabOrder(self.edtType, self.edtName)
        dialogsend.setTabOrder(self.edtName, self.edtTags)
        dialogsend.setTabOrder(self.edtTags, self.btnSearch)
        dialogsend.setTabOrder(self.btnSearch, self.cbPrefix)
        dialogsend.setTabOrder(self.cbPrefix, self.edtMsg)
        dialogsend.setTabOrder(self.edtMsg, self.edtPic)
        dialogsend.setTabOrder(self.edtPic, self.btnBrowse)
        dialogsend.setTabOrder(self.btnBrowse, self.txtLog)
        dialogsend.setTabOrder(self.txtLog, self.btnStartWechat)
        dialogsend.setTabOrder(self.btnStartWechat, self.btnStartSend)
        dialogsend.setTabOrder(self.btnStartSend, self.btnUpdateContacts)

    def retranslateUi(self, dialogsend):
        _translate = QtCore.QCoreApplication.translate
        dialogsend.setWindowTitle(_translate("dialogsend", "群发管理"))
        self.label_5.setText(_translate("dialogsend", "省份："))
        self.label_4.setText(_translate("dialogsend", "城市："))
        self.label_8.setText(_translate("dialogsend", "备注："))
        self.label_7.setText(_translate("dialogsend", "标签："))
        self.label_6.setText(_translate("dialogsend", "性别："))
        self.btnSearch.setText(_translate("dialogsend", "查找过滤"))
        self.label_2.setText(_translate("dialogsend", "类型："))
        self.label_9.setText(_translate("dialogsend", "名字："))
        self.label.setText(_translate("dialogsend", "发送文本："))
        self.cbPrefix.setText(_translate("dialogsend", "使用称呼(文本里用%s代替)"))
        self.edtMsg.setHtml(_translate("dialogsend", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%s你好，这是一条测试信息</p></body></html>"))
        self.label_3.setText(_translate("dialogsend", "发送图像："))
        self.btnBrowse.setText(_translate("dialogsend", "..."))
        self.btnStartWechat.setText(_translate("dialogsend", "启动微信"))
        self.btnStartSend.setText(_translate("dialogsend", "开始发送"))
        self.btnUpdateContacts.setText(_translate("dialogsend", "更新通讯录"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialogsend = QtWidgets.QDialog()
    ui = Ui_dialogsend()
    ui.setupUi(dialogsend)
    dialogsend.show()
    sys.exit(app.exec_())

