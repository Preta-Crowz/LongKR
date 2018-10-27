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
    dat['skin'] = info[7]
    return dat



def check_url(code):
    if not code_vaild(code): return False
    db = sqlite3.connect(f'{config["DB_NAME"]}.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM urls WHERE code=\"{}\"".format(code))
    return cur.fetchall() != []



def get_url(code):
    db = sqlite3.connect(f'{config["DB_NAME"]}.db')
    cur = db.cursor()
    cur.execute("SELECT redirect FROM urls WHERE code=\"{}\"".format(code))
    return cur.fetchall()[0]



def id_vaild(test):
    try: return re.match(r'^[A-Za-z0-9\-\_]+$',test)[0] == test
    except: return False

def mail_vaild(test):
    try: return re.match(r'^[^;]+\@[^;]+(\.[^;]+)+$',test) != None
    except: return False

def code_vaild(test):
    try: return re.match(r'^[가-힣\-\_]+$',test)[0] == test
    except: return False

def vaild(test):
    try: return re.match(r'^[^;]+$',test)[0] == test
    except: return False



def get_skins():
    f = os.listdir("file")
    f.remove("index.txt")
    i = os.listdir("img")
    i.remove("index.txt")
    t = os.listdir("templates")
    t.remove("index.txt")
    fit = f+i+t
    skins = set()
    for item in set(fit):
        if fit.count(item) == 3: skins.add(item)
    return list(skins)