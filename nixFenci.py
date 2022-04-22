#!/usr/bin/ python3

# -*- coding: utf-8 -*-

"""

@author: anhy

@file  : nixFenci.py

@time  : 2022/4/22 12:23

@desc  :

"""


def cizai(qieci, cilist):
    tmp_w = qieci
    tmp_len = len(tmp_w)
    ci_W = ''
    while tmp_len >= 1:
        if tmp_w in cilist:
            ci_W = tmp_w
            break
        else:
            tmp_len = tmp_len - 1
            tmp_w = tmp_w[-tmp_len:]
    return ci_W


juzi = "南京市长江大桥欢迎您"
ci_list = ["南京", "南京市", "长江大桥", "大桥", "市长", "江大桥", "南京市", "欢迎您", "欢迎", "您"]


out_list = []
tmp_ju = juzi
ju_len =  len(tmp_ju)
while ju_len >= 5:
    tmp_w = tmp_ju[-5:]
    chaici = cizai(tmp_w, ci_list)
    out_list.append(chaici)
    tmp_ju = tmp_ju[:-len(chaici)]
    ju_len = ju_len - len(chaici)

while ju_len >= 1:
    chaici = cizai(tmp_ju, ci_list)
    out_list.append(chaici)
    tmp_ju = tmp_ju[:-len(chaici)]
    ju_len = ju_len - len(chaici)

out_list.reverse()
out = ""
if out_list:
    for i in range(len(out_list)):
        out = out + str(out_list[i]) + "-"
print(out)










