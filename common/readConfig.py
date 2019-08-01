#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/1 11:21
# @Author  : z.g

import configparser
import os


def get_conf(section, param):
    root_dir = os.path.abspath('.')
    configpath = os.path.join(root_dir, "config.ini")
    cf = configparser.ConfigParser()
    cf.read(configpath)

    value = cf.get(section,param)
    return value

# print(get_conf("ENV","host"))

#
# class ReadConfig:
#     """定义一个读取配置文件的类"""
#
#     def __init__(self, filepath=None):
#         if filepath:
#             configpath = filepath
#         else:
#             root_dir = os.path.abspath('.')
#             configpath = os.path.join(root_dir, "config.ini")
#         self.cf = configparser.ConfigParser()
#         self.cf.read(configpath)
#
#     def get_env(self, section, param):
#         value = self.cf.get(section, param)
#         return value
#
# if __name__ == '__main__':
#     test = ReadConfig()
#     t = test.get_env("ENV","host")
#     print(t)