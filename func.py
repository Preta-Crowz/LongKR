# -*- coding: utf-8 -*-

import secrets
import string
import bcrypt
import time
import re
import sqlite3
import json
config = json.load(open("config.json"))

def get_random(length):
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))



def register(account,password,nickname,mail):
    db = sqlite3.connect(f'{config["DB_NAME"]}.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM user WHERE account=\"{}\"".format(account))
    if cur.fetchall() != []:
        db.commit()
        return False
    if nickname is None: nickname = account
    pwhash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    now = time.time()
    dat = (account,nickname,pwhash,now,mail,False,now,config['DEF_SKIN'])
    cur.execute('INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?, ?)',dat)
    db.commit()
    return True



def login(account,password):
    db = sqlite3.connect(f'{config["DB_NAME"]}.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM user WHERE account=\"{}\"".format(account))
    info = cur.fetchall()
    if info == []:
        return False
    hashed = info[0][2]
    if bcrypt.checkpw(password.encode(), hashed.encode()):
        now = time.time()
        cur.execute('UPDATE user SET last=(?) WHERE account=(?)',(now,account))
        db.commit()
        return True
    return False



def get_user(account):
    db = sqlite3.connect(f'{config["DB_NAME"]}.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM user WHERE account=\"{}\"".format(account))
    info = cur.fetchall()
    if info == []:
        return {}
    info = info[0]
    dat = {}
    dat['account'] = info[0]
    dat['username'] = info[1]
    dat['created'] = info[3]
    dat['mail'] = info[4]
    dat['admin'] = info[5]
    dat['last_login'] = info[6]
    return dat



def id_vaild(test):
    return re.match(r'^[A-Za-z0-9\-\_]+$',test)[0] == test

def mail_vaild(test):
    return re.match(r'^[^;]+\@[^;]+(\.[^;]+)+$',test) != None

def vaild(test):
    return re.match(r'^[^;]+$',test)[0] == test