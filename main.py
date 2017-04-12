from PyQt5 import QtWidgets
from mainwindow_imp import mainwindow_imp
import sys, getopt
import shutil
import itchat
from wxHelper import *
from itchat.content import *

if __name__ == "__main__":

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)

    wxInst = itchat.new_instance()
    wxHelper = wxHelper(wxInst, 5)

    hotload = 'wxbatch'
    dbfile = "wechat.db"
    monitor = False
    fetchMobile=False
    uimode = True

    opts, args = getopt.getopt(sys.argv[1:], "i:db:m:f:u:")
    for op, value in opts:
        if op == "-i":
            hotload += value
        elif op=="-db":
            dbfile = value
        elif op=="-m":
            monitor = (value=='Y')
        elif op=="-f":
            fetchMobile = (value=='Y')
        elif op=="-u":
            uimode = (value=='Y')

    wxHelper.DBFILE = dbfile
    if not os.path.exists(dbfile):
        shutil.copyfile('wechat_em.db', dbfile)

    if fetchMobile:
        wxHelper.get_mobile_from_fields()

    wxInst.auto_login(hotReload=True, statusStorageDir=hotload)

    if monitor:
        savedir = 'temp'
        os.makedirs(savedir, exist_ok=True)

        @wxInst.msg_register(TEXT, isFriendChat=True)
        def reply(msg):
            print("%s said: %s" % (msg['User']['NickName'], msg['Text']))

        @wxInst.msg_register(TEXT, isGroupChat=True)
        def reply(msg):
            print("%s [:] %s said: %s" % (msg['User']['NickName'], msg['ActualNickName'], msg['Text']))

        @wxInst.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
        def reply(msg):
            msg['Text'](savedir+'\\'+msg['FileName'])
            print("%s sent: %s" % (msg['User']['NickName'], savedir+'\\'+msg['FileName']))

        @wxInst.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
        def reply(msg):
            msg['Text'](savedir+'\\'+msg['FileName'])
            print("%s [:] %s sent: %s" % (msg['User']['NickName'], msg['ActualNickName'], savedir+'\\'+msg['FileName']))

    wxInst.run(blockThread=False)
    wxInst.dump_login_status(hotload)
    if uimode:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = mainwindow_imp(wxInst, wxHelper)
        MainWindow.setupUi(MainWindow)

        MainWindow.showMaximized()
        sys.exit(app.exec_())
    elif monitor:
        while True:
            time.sleep(1)
            cmd = input("CMD:")
            if cmd == 'quit':
                wxInst.logout()
                logging.info("quitting....")
                exit()
