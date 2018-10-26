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



def id_vaild(test):
    return re.match(r'^[A-Za-z0-9\-\_]+$',test)[0] == test

def mail_vaild(test):
    return re.match(r'^[^;]+\@[^;]+(\.[^;]+)+$',test) != None

def vaild(test):
    return re.match(r'^[^;]+$',test)[0] == test