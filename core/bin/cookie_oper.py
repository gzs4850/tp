#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/3 14:07
# @Author  : z.g
import os

# 读取cookie
def get_cookie():
    # PATH = os.getcwd()
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))+'/cookie.txt'
    with open(file, 'rb') as f:
        cookie = f.read().decode()
    return cookie.strip("\n")


if __name__ == '__main__':
    print(os.path.abspath(__file__))