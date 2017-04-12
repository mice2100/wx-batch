#!/usr/bin/env python
# coding: utf-8
import itchat
import logging.config
import threading
import os
import json, sqlite3
import time, re, copy


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
    def __init__(self, wxInst, intval=2):
        self.chat = wxInst
        self.sendJobs = []
        self.event_send = threading.Event()
        self.lock_send = threading.RLock()
        self.thread_send = None
        self.toaddfriends = []
        self.lock_addfriend = threading.RLock()
        self.event_add_friend = threading.Event()
        self.add_friend_cnt = 5
        self.thread_add_friend = None
        self.DBFILE = ''
        self.JOBFILE='JOBS.JSON'
        self.interval = intval

    def start_batchsend(self):
        if os.path.exists(self.JOBFILE):
            self.lock_send.acquire()
            try:
                self.sendJobs = json.load(open(self.JOBFILE))
            except:
                self.sendJobs = []
                os.remove(self.JOBFILE)
            finally:
                self.lock_send.release()

        self.event_send.clear()
        self.thread_send = threading.Thread(target=self.batchSendProc)
        self.thread_send.start()

    def add_send_jobs(self, jobs):
        self.lock_send.acquire()
        tmp = copy.deepcopy(jobs)
        self.sendJobs.append(tmp)
        self.lock_send.release()

    def batchSendProc(self):
        logging.info('[*] 进入群发模式 ... 成功')
        try:
            while not self.event_send.wait(self.interval):
                self.lock_send.acquire()

                if len(self.sendJobs)<=0:
                    self.lock_send.release()
                    continue
                jobd = self.sendJobs[0]

                count = len(jobd['receipts'])
                if count<=0:
                    self.sendJobs.pop(0)
                    self.lock_send.release()
                    continue

                MSG = jobd['msg'] or ""
                PIC = jobd['pic'] or ""
                PIC2 = jobd['pic_2'] or ""
                PIC3 = jobd['pic_3'] or ""
                PREFIX = jobd['prefix'] or 1

                # logging.debug("%s, %s", MSG, PIC)
                import os
                if 'media_id' not in jobd and os.path.exists(PIC):
                    media = self.chat.upload_file(PIC, isPicture=True)
                    jobd['media_id'] = media['MediaId']
                if 'media_id2' not in jobd and os.path.exists(PIC2):
                    media = self.chat.upload_file(PIC2, isPicture=True)
                    jobd['media_id2'] = media['MediaId']
                if 'media_id3' not in jobd and os.path.exists(PIC3):
                    media = self.chat.upload_file(PIC3, isPicture=True)
                    jobd['media_id3'] = media['MediaId']

                row = jobd['receipts'][0]

                usr = self.chat.search_friends(remarkName=row['remark'], nickName=row['nickname'], wechatAccount=row['alias'])
                if len(usr) == 0:
                    usr = self.chat.search_chatrooms(row['nickname'])
                    if len(usr) == 0:
                        jobd['receipts'].pop(0)
                        self.lock_send.release()
                        logging.debug("cant find user or chatroom")
                        continue
                uid = usr[0]['UserName']

                if len(MSG) > 0:
                    msg = MSG
                    if PREFIX >1:
                        prefix = row['prefix'] or ""
                        msg = MSG % prefix
                    logging.info("Sending 1/%d msg: %s", count, msg)
                    self.chat.send_msg(msg, uid)
                if 'media_id' in jobd:
                    logging.info("Sending 1/%d image %s", count, PIC)
                    self.chat.send_image(toUserName=uid, mediaId=jobd['media_id'], fileDir=PIC)
                if 'media_id2' in jobd:
                    logging.info("Sending 1/%d image %s", count, PIC2)
                    self.chat.send_image(toUserName=uid, mediaId=jobd['media_id2'], fileDir=PIC2)
                if 'media_id3' in jobd:
                    logging.info("Sending 1/%d image %s", count, PIC3)
                    self.chat.send_image(toUserName=uid, mediaId=jobd['media_id3'], fileDir=PIC3)

                jobd['receipts'].pop(0)
                if len(self.sendJobs) > 0 and len(self.sendJobs[0]['receipts']) > 0:
                    with open(self.JOBFILE, 'w') as f:
                        f.write(json.dumps(self.sendJobs))
                self.lock_send.release()

        except Exception as e:
            self.lock_send.release()
            logging.exception(str(e))

        logging.info('[*] 退出群发模式 ...')

    def stop_batchsend(self):
        if self.thread_send:
            self.event_send.set()
            self.thread_send.join(10)
            self.thread_send = None

    def saveContact(self):
        tp = [self.chat.get_friends(), self.chat.get_chatrooms(), self.chat.get_mps()]
        import sqlite3
        con = sqlite3.connect(self.DBFILE)
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
