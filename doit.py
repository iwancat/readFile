#!/usr/bin/ python3

# -*- coding: utf-8 -*-

"""

@author: anhy

@file  : doit.py

@time  : 2022/2/22 18:00

@desc  :

"""
import re
import os
import sys
import time

import logtools2

# 日志路径 -需要创建目录
logs = logtools2.LoggerHandler("/Users/yuehaoan/data/pcstatiot/", "statiot.")
# logs.info("hellpdfffffdd")
# 入口路径 -入口目录不存在会退出进程
dofilepath = "/Users/yuehaoan/data/stat/xfer_pcs/xfer_pcs/"
# 出口路径 -程序会创建出口路径
writefilepath = "/Users/yuehaoan/data/stat/xfer_pcs/xfer_pcs/output/"
# 匹配规则
regexx = re.compile('^xfer_npcs.*stat.[0-9]{6}')
# 扫描间隔 写30就是代表30s  单位是秒
saohuang = 30

def getFileList(path, rex):
    """历史迭代，目前不用"""
    filelist = []
    # regexd = re.compile('[0-9]{6}')
    for home, dirs, files in os.walk(path):
        # for dirr in dirs:
        #     if not re.findall(regexd, dirr):
        #         print(dirr)
        for filename in files:
            # print(filename)
            if not re.findall(rex, filename):
                logs.debug("不匹配的文件"+filename)
                continue
            else:
                logs.info("todofile:"+filename)
                fullname = os.path.join(home, filename)
                filelist.append(fullname)
    # logs.info(filelist)
    return filelist


def getFileList2(path, rex):
    """ 获取目录列表 """
    filelist = []
    regexd = re.compile('[0-9]{6}')
    for dirs in os.listdir(path):
        if not re.findall(regexd, dirs):
            # logs.debug("不匹配的目录"+path+dirs)
            continue
        else:
            # print(dirs)
            dirpaht=path+dirs
            logs.debug("匹配的目录"+dirpaht)
            for filei in os.listdir(dirpaht):
                if not re.findall(rex, filei):
                    # logs.debug("不匹配的文件"+path+dirs+"/"+filei)
                    continue
                else:
                    logs.info("正确匹配的文件"+path+dirs+"/"+filei)
                    filelist.append(path+dirs+"/"+filei)
    return filelist


def shuchuDoc(ofptfun, outfilenamefun, custOpenFilefun, writefilepathfun):
    """
        ofpt 输出临时目录\n
        outfilename 输出文件名\n
        custOpenFile  输出内容\n
        writefilepath 输出出口路径\n
    """
    # 写数据文件到临时目录
    ofntfile = ofptfun+outfilenamefun
    ofnt = open(ofntfile, "w+")
    ofnt.writelines(custOpenFilefun)
    logs.info("write %s done" % ofntfile)
    ofnt.close()

    # 处理完后将跨天入口文件挪名

    # 将数据文件从临时目录挪到输出目录
    ofn = writefilepathfun+outfilenamefun
    try:
        os.rename(ofntfile, ofn)
    except Exception as e:
        logs.error("move file failed, err:%s" % e)
        sys.exit()
    logs.info("move file %s to %s" % (ofntfile, ofn))
    # for of in custOpenFile:
    #     print(of)
    # print(custOpenFile)


def markfile(filePath, headMark):
    # print(filePath)
    # print(headMark)
    ofilep = os.path.split(filePath)
    # oldfilename = filePath.split("/")[-1]
    oldfilename = str(ofilep[1])
    newfilename = headMark+"_"+oldfilename
    newpa = str(ofilep[0])+"/"+str(newfilename)
    # print(newpa)
    try:
        os.rename(filePath, newpa)
    except Exception as e:
        logs.error("mark file failed, err:%s" % e)
        sys.exit()
    logs.info("mark file %s to %s" % (filePath, newpa))


if __name__ == '__main__':

    # 如果入口路径不存在，退出
    if not os.path.exists(dofilepath):
        logs.info("input path not find")
        sys.exit()

    # 出口目录判断是否存在
    if not os.path.exists(writefilepath):
        os.mkdir(writefilepath)
    # 出口临时目录
    ofpt = writefilepath+"process_0001/"
    if not os.path.exists(ofpt):
        os.mkdir(ofpt)

    # 临时记录行号目录.pmt 判断是否存在
    pmtpath = dofilepath+".pmt/"
    pmtpathfile = pmtpath+"npcswash.stat"
    if not os.path.exists(pmtpath):
        os.mkdir(pmtpath)

    while True:
        # 读取记录行号文件pmtpathfile 到字典中
        if os.path.exists(pmtpathfile):
            nftmp = open(pmtpathfile, "r")
            nfofile = nftmp.readlines()
            nftmp.close()
            nftmpdic = {}
            for statline in nfofile:
                lliebiao = statline.split(" ")[0]   # 文件名列  #作为字典的key
                try:
                    lliebiaonum = statline.replace('\n', '').split(" ")[1]   # 文件处理过的行数 #作为字典的value
                except Exception as e:
                    logs.error(e)
                    continue
                nftmpdic[lliebiao] = lliebiaonum
        else:
            nftmpdic = {}

        list = getFileList2(dofilepath, regexx)
        for infile in list:
            # print(file)
            outfilename = infile.split("/")[-1]
            # print("---"+outfilename)

            # 获取当天日期，判断是否为今日文件
            outfilenameday = outfilename.split(".")[-1]
            todayday = time.strftime("%Y%m%d", time.localtime())
            # print(outfilenameday+"===="+todayday)
            if outfilenameday == todayday: # 是今天的文件
                # 判断字典中是否存在当前要处理文件 if不在字典 else在字典
                if outfilename not in nftmpdic.keys():
                    # 读要处理的文件
                    statfile = open(infile, "r")
                    # file_date = time.strftime("%Y%m%d%H%M%S")
                    # logs.info("file date:%s" % file_date + " cust do file "+infile)
                    custOpenFile = statfile.readlines()
                    # print(len(custOpenFile))
                    statfile.close()

                    # 写记录行号文件--现在调整为写字典中，字典在处理完文件列表后统一更新回 记录行号文件中
                    nftmpdic[outfilename] = str(len(custOpenFile))

                    shuchuDoc(ofpt, outfilename, custOpenFile, writefilepath)
                    logs.info("直接处理的文件:"+outfilename+" numbercount:"+str(len(custOpenFile)))
                    # markfile(infile, "ssl") #当日文件不改文件名
                else:
                    # print("ddd")
                    # 获取文件的行号
                    with open(infile, 'r') as f:
                        for filenum, _ in enumerate(f): pass
                    filenum += 1
                    # print(filenum)
                    # 获取字典中的行号
                    siem = nftmpdic.get(outfilename, "nameIsNull")
                    # 如果文件的行号与字典中记录的行号一致，直接改名
                    # print(siem)
                    # 不一致，则重处理，字典的行数值需要更新，行数多了 增量更新，行数少了，退出
                    if int(filenum) == int(siem):
                        logs.info(str(outfilename)+" dicmum:"+str(siem)+"  filenum:"+str(filenum)+"  num count equal. and today file has no change, nothing to do")
                        # 如果一样，则啥也不干 --日志往上一行加一起了
                        # logs.info(str(outfilename)+" today file has no change, nothing to do ")
                        continue
                        # markfile(infile, "ssl") #当日文件不改文件名
                    elif int(filenum) > int(siem):
                        logs.info(str(outfilename)+" dicmum:"+str(siem)+"  filenum:"+str(filenum)+"  num count Unequal, filenum > dicmum, file 增量 add")
                        # 读要处理的文件
                        statfile = open(infile, "r")
                        custOpenFile = statfile.readlines()
                        statfile.close()
                        # print(custOpenFile)

                        zengliangnei = []
                        for siemitem in range(int(siem), len(custOpenFile)):
                            # print(siemitem)
                            zengliangnei.append(custOpenFile[siemitem])
                        # print("==")
                        # print(zengliangnei)
                        # 写记录行号文件--现在调整为写字典中，字典在处理完文件列表后统一更新回 记录行号文件中
                        nftmpdic[outfilename] = str(len(custOpenFile))
                        outfilenameadd = outfilename+".add"+str(time.strftime("%H%M%S", time.localtime()))
                        shuchuDoc(ofpt, outfilenameadd, zengliangnei, writefilepath)
                        logs.info("增量的文件:"+outfilenameadd+" numbercount:"+str(len(zengliangnei)))
                        # markfile(infile, "ssl") #当日文件不改文件名
                    else:
                        logs.info(str(outfilename)+" dicmum:"+str(siem)+"  filenum:"+str(filenum)+"  num count Unequal, filenum < dicmum")
                        sys.exit()
            else:
                # 不是今天的文件
                # 判断字典中是否存在当前要处理文件 if不在字典 else在字典
                if outfilename not in nftmpdic.keys():
                    # 读要处理的文件
                    statfile = open(infile, "r")
                    # file_date = time.strftime("%Y%m%d%H%M%S")
                    # logs.info("file date:%s" % file_date + " cust do file "+infile)
                    custOpenFile = statfile.readlines()
                    # print(len(custOpenFile))
                    statfile.close()

                    # 写记录行号文件--现在调整为写字典中，字典在处理完文件列表后统一更新回 记录行号文件中
                    nftmpdic[outfilename] = str(len(custOpenFile))

                    shuchuDoc(ofpt, outfilename, custOpenFile, writefilepath)
                    logs.info("直接处理的文件:"+outfilename+" numcount:"+str(len(custOpenFile)))
                    markfile(infile, "ssl")
                else:
                    # print("ddd")
                    # 获取文件的行号
                    with open(infile, 'r') as f:
                        for filenum, _ in enumerate(f): pass
                    filenum += 1
                    # print(filenum)
                    # 获取字典中的行号
                    siem = nftmpdic.get(outfilename, "nameIsNull")
                    # 如果文件的行号与字典中记录的行号一致，直接改名
                    # print(siem)
                    # 不一致，则重处理，字典的行数值需要更新，行数多了 增量更新，行数少了，退出
                    if int(filenum) == int(siem):
                        logs.info(str(outfilename)+" dicmum:"+str(siem)+"  filenum:"+str(filenum)+"  num count equal, file not today file,so mark rename")
                        markfile(infile, "ssl")
                    elif int(filenum) > int(siem):
                        logs.info(str(outfilename)+" dicmum:"+str(siem)+"  filenum:"+str(filenum)+"  num count Unequal, filenum > dicmum, file 增量 add")
                        # 读要处理的文件
                        statfile = open(infile, "r")
                        custOpenFile = statfile.readlines()
                        statfile.close()
                        # print(custOpenFile)

                        zengliangnei = []
                        for siemitem in range(int(siem), len(custOpenFile)):
                            # print(siemitem)
                            zengliangnei.append(custOpenFile[siemitem])
                        # print("==")
                        # print(zengliangnei)
                        # 写记录行号文件--现在调整为写字典中，字典在处理完文件列表后统一更新回 记录行号文件中
                        nftmpdic[outfilename] = str(len(custOpenFile))
                        outfilenameadd = outfilename+".add"+str(time.strftime("%H%M%S", time.localtime()))
                        shuchuDoc(ofpt, outfilenameadd, zengliangnei, writefilepath)
                        logs.info("增量的文件:"+outfilenameadd+" numbercount:"+str(len(zengliangnei)))
                        markfile(infile, "ssl")
                    else:
                        logs.info(str(outfilename)+" dicmum:"+str(siem)+"  filenum:"+str(filenum)+"  num count Unequal, filenum < dicmum")
                        sys.exit()


        # print(nftmpdic)

        nftmpdicoutlist = []
        for k,v in nftmpdic.items():
            nftmpdicoutlist.append(k+" "+v+"\n")
        # print(nftmpdicoutlist)
        #将字典nftmpdic中的值写到  记录行号文件pmtpathfile中
        #判断文件是否处理过
        oftmp = open(pmtpathfile, "w+")
        oftmp.writelines(nftmpdicoutlist)
        oftmp.close()
        logs.info("current time:"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        time.sleep(saohuang)


