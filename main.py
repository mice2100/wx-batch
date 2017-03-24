from PyQt5 import QtWidgets
from mainwindow_imp import mainwindow_imp
import os
import shutil


if __name__ == "__main__":
    import sys
    if not os.path.exists('wechat.db'):
        shutil.copyfile('wechat_em.db', 'wechat.db')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainwindow_imp()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
