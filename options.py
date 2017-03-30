# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgOption(object):
    def setupUi(self, dlgOption):
        dlgOption.setObjectName("dlgOption")
        dlgOption.resize(320, 157)
        self.horizontalLayout = QtWidgets.QHBoxLayout(dlgOption)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.edProv = QtWidgets.QLineEdit(dlgOption)
        self.edProv.setObjectName("edProv")
        self.gridLayout.addWidget(self.edProv, 0, 3, 1, 1)
        self.edTags = QtWidgets.QLineEdit(dlgOption)
        self.edTags.setObjectName("edTags")
        self.gridLayout.addWidget(self.edTags, 3, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(dlgOption)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(dlgOption)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.edSex = QtWidgets.QLineEdit(dlgOption)
        self.edSex.setObjectName("edSex")
        self.gridLayout.addWidget(self.edSex, 2, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(dlgOption)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.edCity = QtWidgets.QLineEdit(dlgOption)
        self.edCity.setObjectName("edCity")
        self.gridLayout.addWidget(self.edCity, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(dlgOption)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.btnSearch = QtWidgets.QPushButton(dlgOption)
        self.btnSearch.setDefault(True)
        self.btnSearch.setObjectName("btnSearch")
        self.gridLayout.addWidget(self.btnSearch, 4, 3, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(dlgOption)
        QtCore.QMetaObject.connectSlotsByName(dlgOption)
        dlgOption.setTabOrder(self.edProv, self.edCity)
        dlgOption.setTabOrder(self.edCity, self.edSex)
        dlgOption.setTabOrder(self.edSex, self.edTags)
        dlgOption.setTabOrder(self.edTags, self.btnSearch)

    def retranslateUi(self, dlgOption):
        _translate = QtCore.QCoreApplication.translate
        dlgOption.setWindowTitle(_translate("dlgOption", "查询条件"))
        self.label_4.setText(_translate("dlgOption", "标签:"))
        self.label_3.setText(_translate("dlgOption", "性别:"))
        self.label_2.setText(_translate("dlgOption", "城市:"))
        self.label.setText(_translate("dlgOption", "省份:"))
        self.btnSearch.setText(_translate("dlgOption", "查询"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlgOption = QtWidgets.QDialog()
    ui = Ui_dlgOption()
    ui.setupUi(dlgOption)
    dlgOption.show()
    sys.exit(app.exec_())

