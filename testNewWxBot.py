from wxHelper import *
import itchat


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
    # logging.config.fileConfig("logger.conf")
    # if not sys.platform.startswith('win'):
    #     import coloredlogs
    #     coloredlogs.install(level='DEBUG')

    wxInst = itchat.new_instance()
    bot = wxHelper(wxInst)

    while True:
        time.sleep(1)
        cmd = input("CMD:")
        if cmd=='quit':
            wxInst.logout()
            wxInst.dump_login_status()
            bot.stop_batchsend()
            logging.info("quitting....")
            exit()
        elif cmd=='save':
            bot.saveContact()
        elif cmd=='send':
            bot.start_batchsend()
        elif cmd=='stop':
            wxInst.logout()
            wxInst.dump_login_status()
        elif cmd=='stopsend':
            bot.stop_batchsend()
        elif cmd=='start':
            wxInst.auto_login(hotReload=True)
            wxInst.run(blockThread=False)
        elif cmd=='group':
            bot.add_group_friends('个性化商务印品','你好，我是N8娄志君')
        elif cmd=='stopgroup':
            bot.stop_add_group_members()

