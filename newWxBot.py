#!/usr/bin/env python
# coding: utf-8

from wxBot.wxbot import *
import logging.config
import threading
import os
import json

JOBFILE='job.txt'

def make_cond_from_json(fpath):
    if not os.path.exists(fpath):
        return ""

    condition = json.load(open(fpath))

    SQL = ""
    tt = condition.get('sex')
    if tt != None and len(tt)>0: SQL += "sex=%d and " % tt
    tt = condition.get('province')
    if tt != None and len(tt)>0: SQL += "province='%s' and " % tt
    tt = condition.get('city')
    if tt != None and len(tt)>0: SQL += "city='%s' and " % tt
    tt = condition.get('type')
    if tt != None and len(tt)>0: SQL += "tp in (%s) and " % tt
    tt = condition.get('tags')
    if tt != None and len(tt)>0: SQL += "tags like '%s' and " % tt
    tt = condition.get('name')
    if tt != None and len(tt)>0: SQL += "nickname like '%s' and " % tt
    tt = condition.get('remark')
    if tt != None and len(tt)>0: SQL += "remark like '%s' and " % tt

    if len(SQL)>0: SQL = SQL[:-5]
    return SQL


class newWxBot(WXBot):
    def __init__(self):
        super(newWxBot, self).__init__()
        self.jobQueue = None
        self.event_send = threading.Event()
        self.thread_send = None
        self.thread_run = None
        self.status = 'loginout'

    def handle_msg_all(self, msg):
        time.sleep(1)
        # if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
        #     self.send_msg_by_uid(u'hi', msg['user']['id'])
            # self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            # self.send_file_msg_by_uid("img/1.png", msg['user']['id'])

    def start(self):
        if self.status == 'loginsuccess': return
        self.thread_run = threading.Thread(target=self.run)
        self.thread_run.start()

    def stop(self):
        if self.status == 'loginout': return
        self.stop_batchsend()
        self.status = 'wait4loginout'
        self.thread_run.join(15)

    def start_batchsend(self):
        self.event_send.clear()
        self.thread_send = threading.Thread(target=self.batchSendMode)
        self.thread_send.start()

    def checkJobs(self):
        if not os.path.exists(JOBFILE):
            return [None, None]

        import json
        condition = json.load(open(JOBFILE))

        SQL = "select nickname, prefix, alias, remark from contacts"

        cond = make_cond_from_json(JOBFILE)
        if len(cond)>0: SQL = SQL + ' where '+cond
        # logging.debug(SQL)

        import sqlite3
        con = sqlite3.connect("wechat.db")
        cur = con.cursor()
        cur.execute(SQL)

        rows = cur.fetchall()
        con.close()

        # logging.debug("%d rows got.", len(rows))
        os.remove(JOBFILE)
        # os.rename(JOBFILE, 'job.%d.txt' % time.time())

        return [condition, rows]

    def batchSendMode(self):
        logging.info('[*] 进入群发模式 ... 成功')
        while not self.event_send.wait(2):
            [jobd, selector] = self.checkJobs()
            if jobd is None: continue
            MSG = jobd.get('msg') if jobd.get('msg') is not None else ""
            PIC = jobd.get('pic') if jobd.get('pic') is not None else ""
            PREFIX = jobd.get('prefix')
            media_id = ""
            # logging.debug("%s, %s", MSG, PIC)
            import os
            if len(PIC) > 0 and os.path.exists(PIC):
                media_id = self.upload_media(PIC, True)

            for row in selector:
                lastCheckTs = time.time()
                for name in [row[2], row[3], row[0]]:
                    uid = self.get_user_id(name)
                    if uid is not None and len(uid) > 0: break
                if uid is None or len(uid) == 0: continue

                if len(MSG) > 0:
                    msg = MSG
                    if PREFIX >0:
                        prefix = row[1] if row[1] is not None else ""
                        msg = MSG % prefix
                    logging.info("Sending msg: %s", msg)
                    self.send_msg_by_uid(msg, uid)
                if len(media_id) > 0:
                    logging.info("Sending image %s", PIC)
                    self.send_imgid_msg_by_uid(media_id, uid, PIC)

                if (time.time() - lastCheckTs) <= 4:
                    time.sleep(4-time.time()+lastCheckTs)
        logging.info('[*] 退出群发模式 ...')

    def schedule(self):
    #     self.send_msg(u'刘龙飞', u'测试')
    #     self.send_img_msg_by_uid("temp/wxqr.png", self.get_user_id(u'刘龙飞'))
        time.sleep(1)
    def stop_batchsend(self):
        if self.thread_send:
            self.event_send.set()
            self.thread_send.join(10)
            self.thread_send = None

    def saveContact(self):
        tp = [self.contact_list, self.group_list, self.public_list, self.special_list]
        import sqlite3
        con = sqlite3.connect("wechat.db")
        cur = con.cursor()
        for i in range(4):
            CTN = tp[i]
            if len(CTN) <= 0: continue
            #            logging.info("Now processing type %d:", i)
            for contact in CTN:
                if len(contact['Alias']) > 0:
                    cond = "alias=?"
                    arg = contact['Alias']
                elif len(contact['RemarkName']) > 0:
                    cond = "alias='' and remark=?"
                    arg = contact['RemarkName']
                else:
                    cond = "alias='' and remark='' and nickname=?"
                    arg = contact['NickName']

                try:
                    #                    print("Querying...")
                    cur.execute("select * from contacts where " + cond, [arg])
                    if cur.fetchone() is not None:
                        logging.info("Updating %s" % contact['NickName'])
                        cur.execute(
                            "update contacts set tp=?, nickname=?, flag=?, sex=?, province=?, city=?, alias=?, sns=?, remark=? where " + cond,
                            [i, contact['NickName'], contact['ContactFlag'], contact['Sex'], contact['Province'],
                             contact['City'],
                             contact['Alias'], contact['SnsFlag'], contact['RemarkName'], arg])
                    else:
                        logging.info("Inserting %s ..." % contact['NickName'])
                        cur.execute(
                            "insert into contacts (tp, nickname, flag, sex, province, city, alias, sns, remark) values(?,?,?,?,?,?,?,?,?)",
                            [i, contact['NickName'], contact['ContactFlag'], contact['Sex'], contact['Province'],
                             contact['City'],
                             contact['Alias'], contact['SnsFlag'], contact['RemarkName']])
                except Exception as inst:
                    logging.info(inst)

        con.commit()
        con.close()

