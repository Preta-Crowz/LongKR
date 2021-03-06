# -*- coding: utf-8 -*-

import json
config = json.load(open("config.json"))

import zerologger as zlog
logger = zlog.Logger(config["RAVEN"]["KEY"],config["RAVEN"]["SECRET"],config["RAVEN"]["PROJECT"],config["APPNAME"],config["LOG"])

import time
logger.debug("time imported")
import re
logger.debug("re imported")
import socket
logger.debug("socket imported")
import os
logger.debug("os imported")
import datetime
logger.debug("datetime imported")

from flask import Flask,render_template,request,send_file,redirect,session,url_for
logger.debug("flask imported")
try:
    from winmagic import magic
except:
    import magic
logger.debug("magic imported")
import requests
logger.debug("requests imported")
import urllib3
logger.debug("urllib3 imported")
import sqlite3
logger.debug("sqlite3 imported")

import func
import error
logger.debug("Submodules imported")

logger.info("Setting up application")
app = Flask(config["APPNAME"])
app.secret_key = os.urandom(16)
logger.debug("Current secret key is {}".format(app.secret_key))

import logging
logging.getLogger('werkzeug').setLevel(-100)
logger.debug("Flask logging disabled")


db = sqlite3.connect(f'{config["DB_NAME"]}.db')
cur = db.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS urls(code text, redirect text, owner text, mail text, created int, expire boolean, timer int, open boolean, security boolean, pwhash text)')
cur.execute('CREATE TABLE IF NOT EXISTS user(account text, nickname text, pwhash text, created int, mail text, admin boolean, last int, skin text)')
db.commit()


#   return json.dumps(data, ensure_ascii=False).encode().decode('utf8')
@app.route('/가/<code>', methods=['GET'])
def go(code):
    set_session()
    if func.check_url(code):
        return redirect(func.get_url(code))
    else:
        return skinned('/red_error.html')



@app.route('/가입', methods=['GET', 'POST'])
def register():
    set_session()
    if request.method == 'POST':
        account = request.form.get('id',None)
        password = request.form.get('password',None)
        nickname = request.form.get('nickname',account)
        if not nickname: nickname = account
        mail = request.form.get('mail',None)


        if not account or account == '':
            return skinned('/register.html', error=error.register('empty_id'), i=None, p=password, n=nickname, m=mail)
        elif not func.id_vaild(account):
            return skinned('/register.html', error=error.register('invaild_id'), i=None, p=password, n=nickname, m=mail)

        if not password or password == '':
            return skinned('/register.html', error=error.register('empty_pw'), i=account, p=None, n=nickname, m=mail)

        if not func.vaild(nickname):
            return skinned('/register.html', error=error.register('invaild_nick'), i=account, p=password, n=None, m=mail)

        if mail:
            if not func.mail_vaild(mail):
                return skinned('/register.html', error=error.register('invaild_mail'), i=account, p=password, n=nickname, m=None)

        res = func.register(account,password,nickname,mail)
        if not res:
            return skinned('/register.html', error=error.register('exists'), i=account, p=password, n=nickname, m=mail)
        else:
            return skinned('/registered.html', i=account, p=password, n=nickname, m=mail)
    return skinned('/register.html', error=None)



@app.route('/로그인', methods=['GET', 'POST'])
def login():
    set_session()
    if request.method == 'POST':
        account = request.form.get('id',None)
        password = request.form.get('password',None)



        if not account or account == '':
            return skinned('/login.html', error=error.login('empty_id'), i=None, p=password)

        if not password or password == '':
            return skinned('/login.html', error=error.login('empty_pw'), i=account, p=None)



        res = func.login(account,password)
        if not res:
            return skinned('/login.html', error=error.login('failed'), i=account, p=password)
        else:
            session['logged'] = True
            session['account'] = account
            usr = func.get_user(account)
            session['username'] = usr['username']
            session['skin'] = usr['skin']
            session['admin'] = usr['admin']
            logger.info("{} logged in site on {}".format(session['username'],ip()))
            return redirect(url_for('main'))
    return skinned('/login.html', error=None)



@app.route('/로그아웃', methods=['GET'])
def logout():
    set_session()
    session['logged'] = False
    session.pop('account', None)
    session.pop('username', None)
    session.pop('skin', None)
    return redirect(url_for('main'))



@app.route('/검색', methods=['GET', 'POST'])
def search():
    set_session()
    return skinned('/search.html', q=None)



@app.route('/단축', methods=['GET', 'POST'])
def short():
    set_session()
    query = request.args.get('q', None)
    return skinned('/shorter.html', error=None, q=query, s=None)



@app.route('/목록', methods=['GET', 'POST'])
def urlist():
    set_session()
    if not session['logged']: return redirect(url_for('unauthorize'))
    page = request.args.get('p','1')
    try: page = int(page)-1
    except: page = 0
    if page < 0: page = 0
    user['urls'][amount*page:amount*page+amount]
    return "Work In Progress.."



@app.route('/등록', methods=['GET', 'POST'])
def add_url():
    set_session()
    return "Work In Progress.."



@app.route('/관리', methods=['GET', 'POST'])
def manage():
    set_session()
    return "Work In Progress.."



@app.route('/관리자', methods=['GET', 'POST'])
def admin():
    if not session['admin']: return skinned('/denied.html')
    set_session()
    return "Work In Progress.."



@app.route('/정보', methods=['GET', 'POST'])
def info():
    set_session()
    return "Work In Progress.."



@app.route('/설정', methods=['GET', 'POST'])
def setting():
    if not session['admin']: return skinned('/denied.html')
    set_session()
    return "Work In Progress.."



@app.route('/', methods=['GET'])
def main():
    set_session()
    today = datetime.date.today()
    if today.month == 4 and today.day == 1:
        return '<script type="text/javascript">location.href="http://warning.or.kr/";</script>'
    return skinned('/main.html')





@app.route('/file/<path:sdir>', methods=['GET'])
def load(sdir):
    if sdir == '':
        return redirect(url_for('main'))
    return file('file',sdir)

@app.route('/img/<path:sdir>', methods=['GET'])
def img(sdir):
    if sdir == '':
        return redirect(url_for('main'))
    return file('img',sdir)

@app.route('/glob/<path:sdir>', methods=['GET'])
def glob(sdir):
    if sdir == '':
        return redirect(url_for('main'))
    return file('global',sdir)


def file(mdir,sdir):
    sdir = re.sub('.*/\.\.(?P<dir>.*)','\g<dir>',sdir)

    if sdir.startswith('./'):
        index = 2
    elif sdir.startswith('/'):
        index = 1
    else:
        index = 0

    fdir = mdir + '/' + sdir[index:]
    if mdir != 'global':
        if not session['logged'] or session['skin'] == "DEFAULT":
            skin = config['DEF_SKIN']
        else:
            skin = session['skin']
        fdir = 'templates/' + skin + '/' + fdir

    if fdir.endswith('.css'):
        mime = 'text/css'
    else:
        mime = magic.Magic(mime=True).from_file(fdir)

    if session['logged']:
        user = session['username']
    else:
        user = ip()
    logger.info("{} accessed {}".format(user,fdir))
    return send_file(fdir,mime)

def set_session():
    if not 'logged' in session: session['logged'] = False
    if not 'admin' in session: session['admin'] = False
    return True

def ip(): # Based on openNAMU ip_check
    xff = ""
    try:
        temp = request.headers.getlist("X-Forwarded-For")[0]
        temp = temp.split(":") [:-1]
        for t in temp:
            xff += ":" + t
        xff = xff[1:]
        ip = request.environ.get('HTTP_X_REAL_IP', xff)
    except:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # if str(ip) == str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr)) or str(ip) == '::1':
    #     ip = 'Reverse Proxy or Local'
    return str(ip)

def skinned(template,**k):
    if not session['logged'] or session['skin'] == "DEFAULT":
        skin = config['DEF_SKIN']
    else:
        skin = session['skin']
    if session['logged']:
        user = session['username']
    else:
        user = ip()
    logger.info("{} accessed {} with {}".format(user,template,skin))
    try:
        rdat = render_template(f'{skin}/templates{template}',**k)
    except:
        rdat = redirect(url_for('main'))
    return rdat

def loop():
    logger.info("Starting up..")
    try:
        app.run(host=config['HOST'],port=config['PORT']);
    except:
        logger.exception("Server crashed!")
        logger.info("Restarting server..")
        loop()
loop()