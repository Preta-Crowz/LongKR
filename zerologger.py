import logging
import raven
import datetime

client = None
logger = None


class TestRaven(Exception):
    def __init__(self):
        self.msg = 'User triggered test_raven function.'
    def __str__(self):
        return self.msg

class NotExist(Exception):
    def __init__(self):
        self.msg = 'Raven client or Logger is not exist.'
    def __str__(self):
        return self.msg



def test_raven():
    global client
    if client != None:
        raise NotExist
    try:
        raise TestRaven
    except TestRaven:
        client.captureException()
        return True



def set_reven(self,key,secret,project):
    global client
    client = raven.Client('https://{}:{}@sentry.io/{}'.format(key,secret,project))



class Logger:
    def __init__(self,key,secret,project=__name__,level=0):
        global client
        set_raven(key,secret,project)
        self._logger = logging.Logger(project)
        now = str(datetime.datetime.now())
        date = now[2:10].replace('-','')
        time = now[11:19].replace(':','')
        now = date+'_'+time
        file = logging.FileHandler('log/{}_{}.log'.format(now,project),level=lvl)
        stream = logging.StreamHandler(level=lvl)
        self._logger.addHandler(file)
        self._logger.addHandler(stream)
        self._raven = client

    def debug(self,msg,*args,**kwargs):
        self._logger.debug(msg,*args,**kwargs)

    def info(self,msg,*args,**kwargs):
        self._logger.info(msg,*args,**kwargs)

    def warning(self,msg,*args,**kwargs):
        self._logger.warning(msg,*args,**kwargs)

    def error(self,msg,*args,**kwargs):
        self._logger.error(msg,*args,**kwargs)

    def exception(self,msg,*args,**kwargs):
        self._logger.exception(msg,*args,**kwargs)

    def critical(self,msg,*args,**kwargs):
        self._logger.critical(msg,*args,**kwargs)

    def log(self,lvl,msg,*args,**kwargs):
        self._logger.log(lvl,msg,*args,**kwargs)



def get_logger(name=__name__):
    global logger
    if logger == None:
        logger = Logger(__name__)
    return logger