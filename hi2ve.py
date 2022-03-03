#!/usr/bin/ python3

# -*- coding: utf-8 -*-

"""

@author: anhy

@file  : hi2ve.py.py

@time  : 2022/3/3 10:57

@desc  :

"""
import sasl as sasl
import thrift
import thrift_sasl
from pyhive import hive
#conn = hive.Connection('localhost')
#conn = hive.Connection(host='39.107.110.181', port=10002, auth="NOSASL", username='hive',  database='default')
conn = hive.Connection(host='39.107.110.181', port=10000, username='hadoop', database='guang')
cursor = conn.cursor()
cursor.execute('select * from wei_20211125')

for result in cursor.fetchall():
    print(result)
conn.close()