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
    def __init__(self, wxInst):
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
            while not self.event_send.wait(2):
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

    def get_group_members_into_memdb(self, groupname):
        if not self.chat.alive:
            return

        try:
            con = sqlite3.connect(self.DBFILE)
            cur = con.cursor()
            SQL = "drop table if exists groupmember"
            cur.execute(SQL)
            SQL = "create table groupmember(username TEXT(65), nickname TEXT(256), isfriend INTEGER default(0))"
            cur.execute(SQL)

            cnt_friend = cnt_unknown = 0

            group = self.chat.search_chatrooms(name=groupname)
            if len(group)>0:
                members = self.chat.update_chatroom(userName=group[0]['UserName'])
                # logging.info('Total members: %d', len(members['MemberList']))
                for xx in members['MemberList']:
                    friend = self.chat.search_friends(userName=xx['UserName'])
                    isfriend = 1
                    if friend is None or len(friend)==0:
                        isfriend = 0
                        cnt_unknown += 1
                    else:
                        isfriend = 1
                        cnt_friend += 1
                        # logging.debug("To add: %s" % xx['NickName'])
                    SQL = "insert into groupmember (username, nickname, isfriend) values('%s', '%s', %d)" %(
                        xx['UserName'], xx['NickName'], isfriend )
                    cur.execute(SQL)
        except Exception as e:
            logging.exception(str(e))
        finally:
            con.commit()
            con.close()
            return [cnt_friend, cnt_unknown]

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

    def tag_usernames(self, usernames, tag):
        con = sqlite3.connect(self.DBFILE)
        cur = con.cursor()
        SQL = ""
        try:
            for uname in usernames:
                usr = self.chat.search_friends(userName=uname)
                if usr is not None:
                    nickname = usr['NickName']
                    alias = usr['Alias']
                    remark = usr['RemarkName']

                    SQL = "select tags from contacts where nickname=? and alias=? and remark=?"
                    param = [nickname, alias, remark]
                    cur.execute(SQL, param)
                    rec = cur.fetchone()
                    if rec is not None:
                        tags = []
                        if rec[0] is not None:
                            tags = rec[0].split(';')
                        if tag not in tags:
                            tags.append(tag)
                            strtags = ';'.join(tags)
                            SQL = "update contacts set tags=? where nickname=? and alias=? and remark=?"
                            param = [strtags, nickname, alias, remark]
                            cur.execute(SQL, param)
                            con.commit()
        except Exception as e:
            logging.info(e)
        finally:
            con.close()


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

    def get_mobile_from_fields(self):
        con = sqlite3.connect(self.DBFILE)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from contacts")
        pattern = re.compile(r'1[\d]{10}')

        rec = cur.fetchone()
        while rec:
            m = pattern.search(rec['nickname'])
            mobile = ""
            if m:
                mobile = m.group()
                logging.info("Got %s from %s" %(rec['nickname'], mobile))
            else:
                m = pattern.search(rec['alias'])
                if m:
                    mobile = m.group()
                    logging.info("Got %s from %s" % (rec['alias'], mobile))
                else:
                    m = pattern.search(rec['remark'])
                    if m:
                        mobile = m.group()
                        logging.info("Got %s from %s" % (rec['remark'], mobile))

            if len(mobile)>0:
                try:
                    con.execute(
                        "update contacts set mobile=? where nickname=? and alias=? and remark=?",
                        [mobile, rec['nickname'], rec['alias'], rec['remark']])
                    con.commit()
                except Exception as inst:
                    logging.info(inst)

            rec = cur.fetchone()
        con.close()

