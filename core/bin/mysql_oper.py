#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 21:04
# @Author  : z.g

import pymysql, datetime
from core.bin.config_parse import get_config

class MysqlConnect(object):
    # 魔术方法, 初始化, 构造函数
    def __init__(self):
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
        print("sql: %s" %sql)
        print("data: %s" %data)
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

    mc = MysqlConnect()
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    req_header = {'User-Agent': 'python-requests/2.22.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Content-Length': '95'}
    req_data = {"username": "admin", "password": "e10adc3949ba59abbe56e057f20f883e", "isRememberPwd": "false"}
    print(req_header)
    print(req_data)
    mc.exec_data(
        'insert into testresults(case_id, real_req_head, real_req_json) values(%s, "%s", "%s")' % (1, req_header, req_data))
    # mc.exec_data(
    #     'insert into testresults(case_id, test_result, real_rsp_code, real_req_path, real_req_head, real_req_json, real_rsp_head, real_rsp_json, real_rsp_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)' % (1, 1, '3', '4', '5', '6', '7', '8', '9'))
    # mc.exec('insert into test(id, text) values(%s, %s)' % (1, repr('哈送到附近')))
    # mc.exec_data('insert into test(id, text) values(%s, %s)' % (1, repr('哈送到附近')))
    # mc.exec_data('insert into test(id, text) values(%s, %s)',(13, '哈送到附近'))
    # mc.select('select * from test')