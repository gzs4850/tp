#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 9:06
# @Author  : z.g

import logging
import time
import sys
import os


class LogConfig:
    def __init__(self, path):
        """
        日志配置
        :param path: 路径
        """

        runtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        mk_dir(path + "/log")
        logfile = path + "/log/" + runtime + '.log'
        logfile_err = path + "/log/" + runtime + '_error.log'

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.handlers = []

        # 第二步，创建一个handler，用于写入全部info日志文件

        fh = logging.FileHandler(logfile, mode='a+')
        fh.setLevel(logging.DEBUG)

        # 第三步，创建一个handler，用于写入错误日志文件

        fh_err = logging.FileHandler(logfile_err, mode='a+')
        fh_err.setLevel(logging.ERROR)

        # 第四步，再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)

        # 第五步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        fh_err.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 第六步，将logger添加到handler里面
        logger.addHandler(fh)
        logger.addHandler(fh_err)
        logger.addHandler(ch)

def mk_dir(path):
    # 去除首位空格
    path = path.strip()
    path = path.rstrip("\\")
    path = path.rstrip("/")

    # 判断路径是否存在
    is_exists = os.path.exists(path)

    if not is_exists:
        try:
            os.makedirs(path)
        except Exception as e:
            logging.error("logs目录创建失败：%s" % e)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        logging.debug("logs目录已存在：%s" % str(path))
        pass