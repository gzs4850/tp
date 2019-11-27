#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 17:47
# @Author  : z.g

import configparser
import os

root_dir = os.path.abspath('.')
configpath = os.path.join(root_dir, "config.ini")

config = configparser.ConfigParser()
config.read(configpath)

# section = config.sections()
# base_url = config.get("ENV", "host")
# print(base_url)

def get_config(section, option):
    return config.get(section, option)


if __name__ == '__main__':
    value = get_config("ENV", "host")
    print(value)