#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/3 14:07
# @Author  : z.g
import os

# 读取cookie
def get_cookie():
    PATH = os.getcwd()
    file = PATH + '/cookie.txt'
    with open(file, 'rb') as f:
        cookie = f.read().decode()
    return cookie.strip("\n")
