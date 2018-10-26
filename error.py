# -*- coding: utf-8 -*-

def register(code):
    if code == 'empty_id': return "아이디를 입력하세요."
    elif code == 'invaild_id': return "아이디가 잘못되었습니다."
    elif code == 'empty_pw': return "비밀번호를 입력하세요."
    elif code == 'invaild_nick': return "닉네임이 잘못되었습니다."
    elif code == 'invaild_mail': return "메일이 잘못되었습니다."
    elif code == 'exists': return "이미 존재하는 계정입니다."
    else: return "알 수 없는 오류가 발생했습니다."