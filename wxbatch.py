from PyQt5 import QtWidgets
from mainwindow_imp import mainwindow_imp
import sys, getopt
import shutil
from wxHelper import *
_VERSION_ = '2.0.1'

if __name__ == "__main__":

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)

    wxInst = itchat.new_instance()
    wxHelper = wxHelper(wxInst)

    hotload = 'wxbatch'
    dbfile = "wechat.db"
    wxHelper.DBFILE = dbfile
    if not os.path.exists(dbfile):
        shutil.copyfile('wechat_em.db', dbfile)

    wxInst.auto_login(hotReload=True, statusStorageDir=hotload)
    import requests, json
    myself = wxInst.search_friends()
    param = {'nickname':myself['NickName']}
    body = json.loads(requests.get('http://f1.nemoinfo.com/N8CloudServer/checkupdate.php', param).text)
    exist = body['EXIST'] or 0
    if exist == 0:
        logging.info('确保使用的是最新软件，请先关注公众号：N8软件[一天后生效]。')
        exit(1)
    version = body['VERSION'] or "1.0.0"
    url = body['URL'] or ''
    if version>_VERSION_:
        logging.info('发现有版本更新，请到如下地址下载: %s' % url)

    wxInst.run(blockThread=False)
    wxInst.dump_login_status(hotload)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = mainwindow_imp(wxInst, wxHelper)
    MainWindow.setupUi(MainWindow)

    MainWindow.showMaximized()
    sys.exit(app.exec_())