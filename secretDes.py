#!/usr/bin/ python3

# -*- coding: utf-8 -*-

"""

@author: anhy

@file  : secretDes.py

@time  : 2022/4/7 17:54

@desc  :

"""

from pyDes import *
import binascii
import argparse

KEY = 'KEYSTORE'
def desEncrypt(strText):
    """
    DES 加密
    :param strText:
    :return:
    """
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(strText, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en).decode()

def desDecrypt(strText):
    """
    DES 解密
    :param strText:
    :return:
    """
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    try:
        de = k.decrypt(binascii.a2b_hex(strText), padmode=PAD_PKCS5)
    except Exception as e:
        print("Decryption failed. Please confirm whether the input encryption string or "
              "encryption method is correct. The current error is: {}".format(e))
        sys.exit(1)
    return de.decode()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", action="store", dest="E_string",
                        help="Please pass a string that needs to be encrypted")
    parser.add_argument("-d", action="store", dest="D_string",
                        help="Please pass the string to be decrypted")
    result = parser.parse_args()

    if result.E_string:
        resultString = desEncrypt(result.E_string)
        print(resultString)
    if result.D_string:
        resultString = desDecrypt(result.D_string)
        print(resultString)