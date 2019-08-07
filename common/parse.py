#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 14:34
# @Author  : z.g

import re
from common.func import *

global var_dict, extract_dict
var_dict = {}
extract_dict = {}

def field_extract(response, extract_dict):
    if isinstance(response, tuple):
        for item in response:
            if isinstance(item, dict):
                print(item)

                for key in extract_dict:
                    pass


extract_dict = {"code": "code", "userId": "data.userId"}

response = (200, {'code': '000', 'errorMsg': '', 'data': {'userId': 2, 'username': 'admin', 'password': 'e10adc3949ba59abbe56e057f20f883e', 'orgId': 1, 'userStatus': 1, 'createId': 123, 'createTime': '2019-05-25 11:52:26', 'modifyId': 2, 'modifyTime': '2019-05-25 11:52:26', 'orgType': 'Corp', 'defaultAppCode': 'seventyfifty', 'allSys': ['seventyfifty', 'permission'], 'orgName': '中铝集团', 'sessionId': 'ca115663-2c94-4168-bf1f-a6f0cec40b4f'}, 'message': None, 'status': None})

field_extract(response, extract_dict)

# print(regex_findall_functions("${func(a=1, b=2)}"))

testcase = '{"request": {"url": "/ajaxLogin/abc${get_randint(min=1, max=100)}/${efg}", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"${get_currenttime()}${ffff}${random_str(randomlength=5)}","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": [{"comparator": "equals", "check": "code", "expected": "000"}]}'

var_dict = {"efg":"5555","ffff":"123"}

def parseVariable(testcase):
    vars = re.findall(r"\$\{\w+\}",testcase)
    for var in vars:
        a = var.lstrip("${").rstrip("}")
        print(a)
        testcase = testcase.replace(var,var_dict.get(a))
        print("testcase:%s" % testcase)

# parseVariable(testcase)

def parseFunc(testcase):
    funcs = re.findall(r"\$\{\w+\(+.*?\)+.*?\}", testcase)
    for func in funcs:
        a = func.lstrip("${").rstrip("}")
        print(a)
        print(eval(a))
        testcase = testcase.replace(func,str(eval(a)))
        print("testcase:%s" %testcase)