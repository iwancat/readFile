#!/usr/bin/ python3

# -*- coding: utf-8 -*-

"""

@author: anhy

@file  : logtool.py

@time  : 2021/12/2 14:37

@desc  :

"""

import os
import time
import logging


def logInfo(logDir):
    logFileNameTime = time.strftime("%Y-%m-%d", time.localtime())
    logFileName = os.path.join(logDir, "kpiSendKafka." + logFileNameTime)
    logging.basicConfig(filename=logFileName,
                        level=logging.INFO,
                        format="%(asctime)s %(filename)s %(funcName)s %(levelname)s %(processName)s"
                               " %(process)s %(message)s"
                        )


""" 引用方式
from getfile import logtool
import logging


lg = logtool.logInfo("/Users/yuehaoan/data/pcstatiot")
logging.info("test")
"""