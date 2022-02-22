#!/usr/bin/ python3

# -*- coding: utf-8 -*-

"""

@author: anhy

@file  : logtools3.py

@time  : 2021/12/15 17:15

@desc  :

"""
import os
import logging
import logging.handlers
import time
import sys

class PublicFun(object):

    def set_log2(self, logpath, logname):
        """
        :param logpath:
        :param logname:

        :return:
        """
        if not os.path.exists(logpath):
            print("logpath:%s not exist!" % logpath)
            sys.exit()
        level = 'INFO'
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        filename = logpath + '/' + logname + time.strftime('%Y%m%d', time.localtime(time.time())) + '.log'
        fh2 = logging.handlers.TimedRotatingFileHandler(filename, 'D', 1, 0)
        fh2.suffix = "%Y%m%d-%H%M%S.log"
        # fh.setLevel(level)
        formatter = logging.Formatter("%(asctime)s %(levelname)s " "[%(module)s.%(funcName)s:%(lineno)d] "
                                      "%(message)s")
        fh2.setFormatter(formatter)
        self.logger.addHandler(fh2)


        sh2 = logging.StreamHandler()
        sh2.setLevel(logging.INFO)
        sh2.setFormatter(formatter)
        self.logger.addHandler(sh2)

        # logging.info("set logger down")
        return self.logger


'''
    引用方式
    import logtools3
    import logging


    p1 = logtools3.PublicFun()
    p1.set_log2("/Users/yuehaoan/data/pcstatiot/", "logtools32_")
    logging.info("log222222222222")
    logging.error("deerrrr")
'''