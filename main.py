from PyQt5 import QtWidgets
from mainwindow_imp import mainwindow_imp
import sys, getopt
import shutil
import itchat
from wxHelper import *
from itchat.content import *
_VERSION_ = '2.0.1'

if __name__ == "__main__":

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)

    wxInst = itchat.new_instance()
    wxHelper = wxHelper(wxInst)

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

    import requests, json
    myself = wxInst.search_friends()
    param = {'nickname': myself['NickName']}
    body = json.loads(requests.get('http://f1.nemoinfo.com/N8CloudServer/checkupdate.php', param).text)
    exist = body['EXIST'] or 0
    if exist == 0:
        logging.info('确保使用的是最新软件，请先关注公众号：N8软件[一天后生效]。')
        exit(1)
    version = body['VERSION'] or "1.0.0"
    url = body['URL'] or ''

    if version > _VERSION_:
        logging.info('发现有版本更新，请到如下地址下载: %s' % url)

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

