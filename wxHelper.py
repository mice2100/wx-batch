#!/usr/bin/env python
# coding: utf-8
import itchat
import logging.config
import threading
import os
import json
import time


def make_cond_from_dict(dict):
    if dict is None: return ""
    SQL = ""
    tt = dict.get('sex')
    if tt is not None and len(tt)>0: SQL += "sex=%s and " % tt
    tt = dict.get('province')
    if tt is not None and len(tt)>0: SQL += "province='%s' and " % tt
    tt = dict.get('city')
    if tt is not None and len(tt)>0: SQL += "city='%s' and " % tt
    tt = dict.get('type')
    if tt is not None and len(tt)>0: SQL += "tp in (%s) and " % tt
    tt = dict.get('tags')
    if tt is not None and len(tt)>0: SQL += "tags like '%s' and " % tt
    tt = dict.get('name')
    if tt is not None and len(tt)>0: SQL += "nickname like '%s' and " % tt
    tt = dict.get('remark')
    if tt is not None and len(tt)>0: SQL += "remark like '%s' and " % tt

    if len(SQL)>0: SQL = SQL[:-5]
    return SQL


def make_cond_from_json(fpath):
    if not os.path.exists(fpath):
        return ""

    condition = json.load(open(fpath))
    return make_cond_from_dict(condition)


class wxHelper:
    def __init__(self, wxInst):
        self.chat = wxInst
        self.sendJobs = []
        self.event_send = threading.Event()
        self.thread_send = None
        self.JOBFILE = 'job.txt'
        self.toaddfriends = []
        self.lock_addfriend = threading.RLock()
        self.event_add_friend = threading.Event()
        self.add_friend_cnt = 5
        self.thread_add_friend = None


    def start_batchsend(self):
        self.event_send.clear()
        self.thread_send = threading.Thread(target=self.batchSendMode)
        self.thread_send.start()

    def jobInQueue(self):
        return os.path.exists(self.JOBFILE)

    def checkJobs(self):
        if not self.jobInQueue():
            return [None, None]

        condition = json.load(open(self.JOBFILE))

        SQL = "select nickname, prefix, alias, remark from contacts"

        cond = make_cond_from_json(self.JOBFILE)
        if len(cond)>0: SQL = SQL + ' where '+cond
        # logging.debug(SQL)

        import sqlite3
        con = sqlite3.connect("wechat.db")
        cur = con.cursor()
        cur.execute(SQL)

        rows = cur.fetchall()
        con.close()

        # logging.debug("%d rows got.", len(rows))
        os.remove(self.JOBFILE)

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
                media = self.chat.upload_file(PIC, isPicture=True)
                media_id = media['MediaId']

            for row in selector:
                lastCheckTs = time.time()
                usr = self.chat.search_friends(remarkName=row[3], nickName=row[0], wechatAccount=row[2])
                if len(usr) == 0:
                    continue
                uid = usr[0]['UserName']

                if len(MSG) > 0:
                    msg = MSG
                    if PREFIX >0:
                        prefix = row[1] if row[1] is not None else ""
                        msg = MSG % prefix
                    logging.info("Sending msg: %s", msg)
                    self.chat.send_msg(msg, uid)
                if len(media_id) > 0:
                    logging.info("Sending image %s", PIC)
                    self.chat.send_image(toUserName=uid, mediaId=media_id, fileDir=PIC)

                if (time.time() - lastCheckTs) <= 2:
                    time.sleep(2-time.time()+lastCheckTs)
        logging.info('[*] 退出群发模式 ...')

    def stop_batchsend(self):
        if self.thread_send:
            self.event_send.set()
            self.thread_send.join(10)
            self.thread_send = None

    def add_group_friends(self, groupname, strhello):
        if not self.chat.alive:
            return
        group = self.chat.search_chatrooms(name=groupname)
        if len(group)>0:
            members = self.chat.update_chatroom(userName=group[0]['UserName'])
            logging.info('Total members: %d', len(members['MemberList']))
            self.lock_addfriend.acquire()
            for xx in members['MemberList']:
                friend = self.chat.search_friends(userName=xx['UserName'])
                if friend is None or len(friend)==0:
                    logging.debug("To add: %s" % xx['NickName'])
                    self.toaddfriends.append([xx['UserName'],strhello,xx['NickName']])
            logging.info('To add friends: %d', len(self.toaddfriends))
            self.lock_addfriend.release()

        if self.thread_add_friend is None:
            self.event_add_friend.clear()
            self.thread_add_friend = threading.Thread(target=self.add_friends_proc())
            self.thread_add_friend.start()

    def stop_add_group_members(self):
        if self.thread_add_friend:
            self.event_add_friend.set()
            self.thread_add_friend.join(10)
            self.thread_add_friend = None

    def add_friends_proc(self):
        signaled = False
        while True:
            self.lock_addfriend.acquire()
            for i in range(self.add_friend_cnt):
                if len(self.toaddfriends) == 0: break

                logging.debug('Adding... %s' % self.toaddfriends[0][2])
                # self.chat.add_friend(self.toaddfriends[0][0], verifyContent=self.toaddfriends[0][1])
                time.sleep(2)
                self.toaddfriends.pop(0)
            self.lock_addfriend.release()

            for lp in range(360):
                signaled = self.event_add_friend.wait(10)
                if signaled: break

        self.thread_add_friend = None

    def saveContact(self):
        tp = [self.chat.get_friends(), self.chat.get_chatrooms(), self.chat.get_mps()]
        import sqlite3
        con = sqlite3.connect("wechat.db")
        cur = con.cursor()
        cur.execute("UPDATE contacts set up2date=0")
        inserted = 0
        for i in range(3):
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
                            "update contacts set up2date=1, tp=?, nickname=?, flag=?, sex=?, province=?, city=?, alias=?, sns=?, remark=? where " + cond,
                            [i, contact['NickName'], contact['ContactFlag'], contact['Sex'], contact['Province'],
                             contact['City'],
                             contact['Alias'], contact['SnsFlag'], contact['RemarkName'], arg])
                    else:
                        logging.info("Inserting %s ..." % contact['NickName'])
                        cur.execute(
                            "insert into contacts (up2date, tp, nickname, flag, sex, province, city, alias, sns, remark) values(1, ?,?,?,?,?,?,?,?,?)",
                            [i, contact['NickName'], contact['ContactFlag'], contact['Sex'], contact['Province'],
                             contact['City'],
                             contact['Alias'], contact['SnsFlag'], contact['RemarkName']])
                        inserted += 1
                except Exception as inst:
                    logging.info(inst)

        con.commit()
        con.close()

        return inserted

