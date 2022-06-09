# -*- coding: utf-8 -*-

"""

@author: liushuai

@file  : jf_mdb_status.py

@time  : 2021/12/01 11:26

@desc  :

"""
import datetime


DAY = datetime.datetime.now()
DAY1 = (DAY - datetime.timedelta(days=1)).strftime('%Y%m%d')
DAY7 = (DAY - datetime.timedelta(days=7)).strftime('%Y%m%d')
DAY30 = (DAY - datetime.timedelta(days=30)).strftime('%Y%m%d')
MONTH = DAY1[0:6]
YESTERDAY = datetime.date.today() - datetime.timedelta(days=1)
TODAY = DAY.strftime('%Y%m%d')


