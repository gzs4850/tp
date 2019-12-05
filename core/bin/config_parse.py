#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 17:47
# @Author  : z.g

import configparser
import os

# section = config.sections()
# base_url = config.get("ENV", "host")
# print(base_url)


def get_config(section, option):
    # root_dir = os.path.abspath('.')
    # configpath = os.path.join(root_dir, "config.ini")
    conf_path = 'D:/code/tp/core/bin/config.ini'
    config = configparser.ConfigParser()
    config.read(conf_path)
    return config.get(section, option)

# class ReadConfig:
#
#     def __init__(self):
#         conf_path = 'D:/code/tp/bin/config.ini'
#         print(conf_path)
#         self.cf = configparser.ConfigParser()
#         self.cf.read(conf_path)
#
#     def get_env(self, param):
#         value = self.cf.get("ENV", param)
#         return value

if __name__ == '__main__':
    value = get_config("ENV", "host")
    print(value)
    # rc = ReadConfig()
    # host = rc.get_env("host")
    # print(host)