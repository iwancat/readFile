#!/usr/bin/ python3

# -*- coding: utf-8 -*-

"""

@author: anhy

@file  : spark2hive.py

@time  : 2022/3/8 14:25

@desc  :

"""

from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import HiveContext
import pandas as pd

import sys
from hdfs.client import Client

def col_spark():
    conf = SparkConf().setAppName("IOT" + "GPRS" + "1")
    sc = SparkContext(conf=conf)
    hc = HiveContext(sc)
    hc.setConf('hive.exec.dynamic.partition.mode', 'nonstrict')
    result = hc.sql("create table duizhang.stat_aaa_2022030901 as select count(1) from duizhang.stat_hc_userlist_4")
    print("===========")
    print(result)
    print("===========")
    result.show()


def write_to_hdfs(client, hdfs_path, data):
    client.write(hdfs_path, data, overwrite=True, append=False, encoding='utf-8')


def col_spark2():
    conf2 = SparkConf().setAppName("IOTAA" + "GPRS" + "2")
    sc2 = SparkContext(conf=conf2)
    hc2 = HiveContext(sc2)
    hc2.setConf('hive.exec.dynamic.partition.mode', 'nonstrict')
    #    sqlong = "create table duizhang.stat_ccc_sp_20220310 as select * from 表 where arrive_time>=20210927170000 and arrive_time<20210927180000"
    sqlong = "select trademark,bill_month,hplmn1,count(1) ddct from duizhang.stat_ccc_sp_20220310 group by trademark,bill_month,hplmn1"
    result2 = hc2.sql(sqlong)
    sslist =  result2.toPandas()

    #filepa = "/home/ochadoop/asiainfo/anhy/spark/slisresult.csv"  #屏蔽写本地
    # ofnt = open(filepa, "w+")       #屏蔽写本地
    hdfile = []
    #ofnt = open(filepa, "w+")        #屏蔽写本地

    for slist in sslist.itertuples():
        linetxt= str(getattr(slist, 'trademark'))+"=====" + str(getattr(slist, 'bill_month')) + "G000000G" + str(getattr(slist, 'hplmn1')) + str(getattr(slist, 'ddct'))+"\n"
        #   ofnt.writelines(linetxt)  #屏蔽写本地
        hdfile.append(linetxt)
    #ofnt.close()                     #屏蔽写本地

    print("next is hdfs write")
    hd_path = "/duizhang/qwmonitor/100-001-002.csv"
    client = Client("http://你的主机ip:50070/", root="/", timeout=10000, session=False)
    client.write(hd_path, hdfile, overwrite=True, append=False, encoding='utf-8')
    print("hdfs is write ok")



'''
    #result2.show(result2.count())

    # result2.collect()
    # print("------------------------")
    # print(result2)
    # print("------------------------")
    # result2.show()
'''

'''
    fields = [StructField("field_name", StringType(), True), StructField("dddd", StringType(), True)]
    schema = StructType(fields)
    df = hc.createDataFrame(result, schema)
    df.createOrReplaceTempView('aleilei')
    mmd = hc.sql("select * from aleilei").show()

    print(mmd)
'''


def mydfs():
    print("next is hdfs list")
    hd_path = "/duizhang"
    client = Client("http://你的ip:50070/", root="/", timeout=10000, session=False)
    client.list(hd_path, status=False)
    print("hdfs is list ok")


if __name__ == '__main__':
    col_spark2()


''' spark-submit启动的命令
PYSPARK_PYTHON=/home/hadoop/apps/Python3/bin/python3 spark-submit \
--master yarn \
--deploy-mode cluster \
--conf spark.yarn.executor.memoryOverhead=4096 \
--num-executors 80 \
--executor-cores 5 \
--executor-memory 20G \
--driver-memory 12G \
--archives hdfs:///duizhang/Python3.zip#ANACONDA \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/home/hadoop/apps/Python3/bin/python3 \
--files /home/ochadoop/apps/spark/conf/hive-site.xml \
spark2hive_sprd.py
'''


