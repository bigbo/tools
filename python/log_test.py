#/*******************************************************************************
# * Author	 : jingbo.li | work at renren-inc.
# * Email	 : ljb90@live.cn
# * Last modified : 2014-03-06 19:37
# * Filename	 : log_test.py
# * Description	 : 
# * *****************************************************************************/
#!/usr/bin/python
#coding=utf-8

import  logging
import logging.config


formatter_dict = {
    1 : logging.Formatter("%(message)s"),
    2 : logging.Formatter("%(levelname)s - %(message)s"),
    3 : logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"),
    4 : logging.Formatter("%(asctime)s - %(levelname)s - %(message)s - [%(name)s]"),
    5 : logging.Formatter("%(asctime)s - %(levelname)s - %(message)s - [%(name)s:%(lineno)s]")
}
class Logger(object):
    def __init__(self, logname, loglevel, callfile):
        '''
            指定日志文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        '''
        self.logger = logging.getLogger(callfile)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(logname)

        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter_dict[int(loglevel)])
        fh.setFormatter(formatter_dict[int(loglevel)])
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    logger = Logger(logname='hahaha', loglevel=1, callfile=__file__).get_logger()  
    logger.info('test level1')
    logger1 = Logger(logname='hahaha2', loglevel=2, callfile=__file__).get_logger()
    logger1.info('test level2')
    '''
    logger2 = Logger(logname='hahaha3', loglevel=3, callfile=__file__).get_logger()
    logger2.info('test level3')
    '''


