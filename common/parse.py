#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 14:34
# @Author  : z.g

import re
from common.func import *

global var_dict, extract_dict
var_dict = {}
extract_dict = {}

testcase = '{"request": {"url": "/ajaxLogin/abc${get_randint(min=1, max=100)}/${efg}", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"${get_currenttime()}${ffff}${random_str(randomlength=5)}","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": {"code": "000","data.userId":"1"}}'

var_dict = {"efg":"5555","ffff":"123"}

exp_dict = {"code": "000","data.userId":"2","data.sec.name":"san"}

extract_dict = {"code1": "code", "userId1": "data.userId", "name":"data.sec.name"}

response = (200, {'code': '000', 'errorMsg': '', 'data': {'userId': 2, 'username': 'admin', 'password': 'e10adc3949ba59abbe56e057f20f883e', 'sec':{'name':'san'},'orgId': 1, 'userStatus': 1, 'createId': 123, 'createTime': '2019-05-25 11:52:26', 'modifyId': 2, 'modifyTime': '2019-05-25 11:52:26', 'orgType': 'Corp', 'defaultAppCode': 'seventyfifty', 'allSys': ['seventyfifty', 'permission'], 'orgName': '中铝集团', 'sessionId': 'ca115663-2c94-4168-bf1f-a6f0cec40b4f'}, 'message': None, 'status': None})


def field_check(testcase,response):
    exp_dict = testcase.get("case_validate")
    response = response[1]
    # print(exp_dict)
    for key in exp_dict.keys():
        # print(key)
        temp = {}
        locator = key.split(".")
        if len(locator) == 1:
            if str(response.get(locator[0])) == str(exp_dict[key]):
                print("check ok %s" %locator[0])
            else:
                print("check fail, expect value is %s, real value is %s" %(exp_dict[key],response.get(locator[0])))
                return False
        else:
            for i in range(len(locator)):
                if i == 0:
                    temp[key] = response.get(locator[i])
                else:
                    temp[key] = temp[key].get(locator[i])
            if str(temp[key]) == str(exp_dict[key]):
                print("check ok %s" % key)
            else:
                print("check fail %s, expect value is %s, real value is %s" % (key, exp_dict[key], temp[key]))
                return False
    return True



def field_extract(response, extract_dict):
    response = response[1]

    for key in extract_dict.keys():
        locator = extract_dict[key].split(".")
        for i in range(len(locator)):
            if i == 0:
                var_dict[key] = response[locator[i]]
            else:
                var_dict[key] = var_dict[key][locator[i]]
    print("var_dict:%s" % var_dict)
    return var_dict

# field_extract(response, extract_dict)

def parseVariable(testcase):
    vars = re.findall(r"\$\{\w+\}",testcase)
    for var in vars:
        a = var.lstrip("${").rstrip("}")
        print(a)
        testcase = testcase.replace(var,var_dict.get(a))
        print("testcase:%s" % testcase)



def parseFunc(testcase):
    funcs = re.findall(r"\$\{\w+\(+.*?\)+.*?\}", testcase)
    for func in funcs:
        a = func.lstrip("${").rstrip("}")
        print(a)
        print(eval(a))
        testcase = testcase.replace(func,str(eval(a)))
        print("testcase:%s" %testcase)



if __name__ == '__main__':
    field_check(exp_dict, response)
    # parseVariable(testcase)
    # parseFunc(testcase)