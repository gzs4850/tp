#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 21:04
# @Author  : z.g

import pymysql
from bin.config_parse import get_config

class MysqlConnect(object):
    # 魔术方法, 初始化, 构造函数
    def __init__(self, host, user, password, database):
        '''
        :param host: IP
        :param user: 用户名
        :param password: 密码
        :param port: 端口号
        :param database: 数据库名
        :param charset: 编码格式
        '''
        host = get_config("MYSQL", "host")
        user = get_config("MYSQL", "user")
        password = get_config("MYSQL", "password")
        port = get_config("MYSQL", "port")
        database = get_config("MYSQL", "database")
        charset = get_config("MYSQL", "charset")
        self.db = pymysql.connect(host=host, user=user, password=password, port=3306, database=database, charset=charset)
        self.cursor = self.db.cursor()

    # 将要插入的数据写成元组传入
    def exec_data(self, sql, data=None):
        # 执行SQL语句
        self.cursor.execute(sql, data)
        # 提交到数据库执行
        self.db.commit()

    # sql拼接时使用repr()，将字符串原样输出
    def exec(self, sql):
        self.cursor.execute(sql)
        # 提交到数据库执行
        self.db.commit()

    def select(self, sql):
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        for row in results:
            print(row)

    # 魔术方法, 析构化 ,析构函数
    def __del__(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    mc = MysqlConnect('127.0.0.1', 'root', '123456', 'ifsys')
    # mc.exec('insert into test(id, text) values(%s, %s)' % (1, repr('哈送到附近')))
    mc.exec_data('insert into test(id, text) values(%s, %s)' % (1, repr('哈送到附近')))
    # mc.exec_data('insert into test(id, text) values(%s, %s)',(13, '哈送到附近'))
    mc.select('select * from test')