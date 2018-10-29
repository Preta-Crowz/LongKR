# -*- coding: utf-8 -*-

from flask import Flask,render_template,request,send_file,redirect,session,url_for
from winmagic import magic
import time
import json
import re
import requests
import socket
import threading
import urllib3
import sqlite3
import os
import datetime

import func
import error
config = json.load(open("config.json"))
app = Flask(__name__)
app.secret_key = os.urandom(16)


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
        return render_template(skinned('/red_error.html'))



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
            return render_template(skinned('/register.html'), error=error.register('empty_id'), i=None, p=password, n=nickname, m=mail)
        elif not func.id_vaild(account):
            return render_template(skinned('/register.html'), error=error.register('invaild_id'), i=None, p=password, n=nickname, m=mail)

        if not password or password == '':
            return render_template(skinned('/register.html'), error=error.register('empty_pw'), i=account, p=None, n=nickname, m=mail)

        if not func.vaild(nickname):
            return render_template(skinned('/register.html'), error=error.register('invaild_nick'), i=account, p=password, n=None, m=mail)

        if mail:
            if not func.mail_vaild(mail):
                return render_template(skinned('/register.html'), error=error.register('invaild_mail'), i=account, p=password, n=nickname, m=None)

        res = func.register(account,password,nickname,mail)
        if not res:
            return render_template(skinned('/register.html'), error=error.register('exists'), i=account, p=password, n=nickname, m=mail)
        else:
            return render_template(skinned('/registered.html'), i=account, p=password, n=nickname, m=mail)
    return render_template(skinned('/register.html'), error=None)



@app.route('/로그인', methods=['GET', 'POST'])
def login():
    set_session()
    if request.method == 'POST':
        account = request.form.get('id',None)
        password = request.form.get('password',None)



        if not account or account == '':
            return render_template(skinned('/login.html'), error=error.login('empty_id'), i=None, p=password)

        if not password or password == '':
            return render_template(skinned('/login.html'), error=error.login('empty_pw'), i=account, p=None)



        res = func.login(account,password)
        if not res:
            return render_template(skinned('/login.html'), error=error.login('failed'), i=account, p=password)
        else:
            session['logged'] = True
            session['account'] = account
            usr = func.get_user(account)
            session['username'] = usr['username']
            session['skin'] = usr['skin']
            session['admin'] = usr['admin']
            return redirect(url_for('main'))
    return render_template(skinned('/login.html'), error=None)



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
    return "Work In Progress.."



@app.route('/단축', methods=['GET', 'POST'])
def short():
    set_session()
    return "Work In Progress.."



@app.route('/목록', methods=['GET', 'POST'])
def urlist():
    set_session()
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
    if not session['admin']: return render_template(skinned('/denied.html'))
    set_session()
    return "Work In Progress.."



@app.route('/정보', methods=['GET', 'POST'])
def info():
    set_session()
    return "Work In Progress.."



@app.route('/설정', methods=['GET', 'POST'])
def setting():
    if not session['admin']: return render_template(skinned('/denied.html'))
    set_session()
    return "Work In Progress.."



@app.route('/', methods=['GET'])
def main():
    set_session()
    today = datetime.date.today()
    if today.month == 4 and today.day == 1:
        return '<script type="text/javascript">location.href="http://warning.or.kr/";</script>'
    return render_template(skinned('/main.html'))





@app.route('/file/<path:sdir>', methods=['GET'])
def load(sdir):
    return file('file',sdir)

@app.route('/img/<path:sdir>', methods=['GET'])
def img(sdir):
    return file('img',sdir)

@app.route('/glob/<path:sdir>', methods=['GET'])
def glob(sdir):
    return file('global',sdir)


def file(mdir,sdir):
    sdir=re.sub('.*/\.\.(?P<dir>.*)','\g<dir>',sdir)
    t=sdir if re.match('(.*/)?.*\..*',sdir) else sdir+'index.html' if sdir.endswith('/') else sdir+'/index.html'
    t=mdir+'/'+sdir[2 if sdir.startswith('./') else 1 if sdir.startswith('/') else 0:]
    return send_file(t,'text/css' if t.endswith('.css') else magic.Magic(mime=True).from_file(t))

def set_session():
    if not 'logged' in session: session['logged'] = False
    if not 'admin' in session: session['admin'] = False

def skinned(template):
    return (session['skin'] if session['logged'] else config['DEF_SKIN'])+template

app.run(host=config['HOST'],port=config['PORT']);