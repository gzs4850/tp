#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 17:30
# @Author  : z.g

import random
from random import Random
import time

def get_currenttime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def get_randint(min = 0, max = 1000):
    return random.randint(min,max)

def random_str(randomlength=31):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

if __name__ == '__main__':
    print(get_currenttime())
    print(random_str(10))
    print(get_randint(0,100))