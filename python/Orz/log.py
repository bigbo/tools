import logging

DEFAULT_FORMATTER = "'%(name)-12s %(asctime)s %(levelname)-8s %(message)s',\
                     '%a, %d %b %Y %H:%M:%S'"

DEFAULT_LOGPATH = '../log/'

LOG_LEVEL={
        'NOTSET'  : 0
        'DEBUG'   : 10,
        'INFO'    : 20,
        'WARNING' : 30,
        'ERROR'   : 40,
        'FATAL'   : 50
        }

DEFAULT_LOG_LEVEL=LOG_LEVEL['INFO']

class log():
    '''un finished'''

    def __init__(
            self,
            name, 
            formatter=DEFAULT_FORMATTER,
            log_path =DEFAULT_LOGPATH,
            level    =DEFAULT_LOG_LEVEL):

        if level.upper() not in LOG_LEVEL.keys():
            raise ...

        self.logger = logging.getLogger(name)
        self.formatter=logging.Formatter(DEFAULT_FORMATTER)
        self.file_handler = logging.FileHandler(DEFAULT_LOGPATH)

        self.file_handler.setFormatter(formatter)
        self.logger.setLevel(LOG_LEVEL[level])

    def info(self , object):
        pass


    def debug(self , object):
        pass

    def warning(self,object):
        pass

    def fatal(self , object):
        pass

    def add_handler(self):
        pass


