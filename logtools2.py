#!/usr/bin/ python3

# -*- coding: utf-8 -*-

"""

@author: anhy

@file  : logtools2.py

@time  : 2021/12/6 11:20

@desc  :

"""
import os
import time
import sys
import logging
import logging.handlers

class LoggerHandler(logging.Logger):

    def __init__(self,
                 pahtlog,
                 filetou,
                 fname=None,
                 level="DEBUG",
                 format="%(asctime)s %(filename)s %(funcName)s %(levelname)s %(processName)s %(process)s %(message)s"
                 ):

        # logger(name)  直接超继承logger当中的name
        super().__init__(fname)

        logFileNameTime2 = time.strftime("%Y-%m-%d", time.localtime())
        name = os.path.join(pahtlog, filetou + logFileNameTime2)
        # 设置收集器级别
        # logger.setLevel(level)
        self.setLevel(level) # 继承了Logger 返回的实例就是自己

        # 初始化format，设置格式
        fmt = logging.Formatter(format)


        #开始写文件
        if not os.path.exists(pahtlog):
            # print(name)
            print("logpath:%s not exist!" % pahtlog)
            # open(name, "a")
            sys.exit()

        #写文件
        print(name)
        # file_handler = logging.FileHandler(name, 'a', encoding='utf-8')
        file_handler = logging.handlers.TimedRotatingFileHandler(name, 'MIDNIGHT', 1, 0)

        # logging.handlers.TimedRotatingFileHandler(filename, 'D', 1, 0)
        # self.logger.addHandler(fh)

        file_handler.setLevel(level)
        self.addHandler(file_handler)
        file_handler.setFormatter(fmt)
        #前台输出
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        self.addHandler(stream_handler)
        stream_handler.setFormatter(fmt)


''' 
引用方式
import logtools2
logs = logtools2.LoggerHandler("/Users/yuehaoan/data/pcstatiot/", "statiot.")

logs.info("hellpdfffffdd")
'''