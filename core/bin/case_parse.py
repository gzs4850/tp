#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 17:22
# @Author  : z.g

import re


#global var_dict, extract_dict
#var_dict = {}
#extract_dict = {}

#testsuit = '[[{"case":{"name":"7050login","request":{"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":{"rspcode":"content.code","username":"content.data.username","token":"content.data.sessionId"},"validate":{"status_code":200,"headers.Content-Type":"application/json;charset=UTF-8","content.code":"000","content.data.username":"admin"},"setup_hooks":[],"teardown_hooks":[]}}}],[{"case":{"name":"7050login","request":{"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":[{"token":"content.data.sessionId"}],"validate":{"status_code":200,"headers.Content-Type":"application/json","content.code":"000"},"setup_hooks":[],"teardown_hooks":[]}}},{"case":{"name":"getUserInfo","request":{"url":"/zlstBigData/permission/user/getUserInfo","method":"GET","headers":{},"json":{},"extract":[],"validate":{"status_code":200,"headers.Content-Type":"application/json","content.code":"000"},"setup_hooks":[],"teardown_hooks":[]}}}]]'

#testcase = '{"request": {"url": "/ajaxLogin/abc${get_randint(min=1, max=100)}/${efg}", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"${get_currenttime()}${ffff}${random_str(randomlength=${value})}","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": {"code": "000","data.userId":"1"}}'

#testcase1 = '{"request": {"url": "/ajaxLogin/abc${get_randint(min=1, max=100)}/5555", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"${get_currenttime()}123${random_str(randomlength=3)}","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": {"code": "000","data.userId":"1"}}'

#var_dict = {"efg":"5555","ffff":"123","value":3}

#exp_dict = {"code": "000","data.userId":"2","data.sec.name":"san"}

#extract_dict = {"code1": "code", "userId1": "data.userId", "name":"data.sec.name"}

#response = (200, {'code': '000', 'errorMsg': '', 'data': {'userId': 2, 'username': 'admin', 'password': 'e10adc3949ba59abbe56e057f20f883e', 'sec':{'name':'san'},'orgId': 1, 'userStatus': 1, 'createId': 123, 'createTime': '2019-05-25 11:52:26', 'modifyId': 2, 'modifyTime': '2019-05-25 11:52:26', 'orgType': 'Corp', 'defaultAppCode': 'seventyfifty', 'allSys': ['seventyfifty', 'permission'], 'orgName': '中铝集团', 'sessionId': 'ca115663-2c94-4168-bf1f-a6f0cec40b4f'}, 'message': None, 'status': None})
variable_dict = "{'username': 'admin', 'access_token': {'content.access_token': None}, 'resultCode': 1}"
case = "{'timeout': 10, 'http_type': 'http', 'host': 'gateway.baolvtest.paas.com', 'case_id': 12, 'case_name': '获取用户信息-admin', 'case_variable': {}, 'case_cookie': None, 'case_url': '/gateway/api-ms/system/users/info', 'case_method': 'GET', 'case_headers':{'Content-Type': 'application/json', 'token': '${access_token}'}, 'case_json': {}, 'case_file': None, 'case_validate': {'content.resultCode': '0'}, 'case_extract': {'resultCode': 'content.resultCode'}, 'setup_hooks': [], 'teardown_hooks': []}"


def parse_variable(variable_dict, case):
    print("---------------开始解析变量-------------------")
    print("variable_dict: %s" %variable_dict)
    print("case: %s" % case)
    vars = re.findall(r"\$\{\w+\}", case)
    if len(vars) > 0:
        for var in vars:
            print("var: %s" %var)
            a = var.lstrip("${").rstrip("}")
            print("a: %s" % a)
            print("str(variable_dict.get(a)): %s" % str(variable_dict.get(a)))
            if isinstance(variable_dict.get(a), dict):
                case = case.replace(var, str(variable_dict.get(a).keys[0]))
            else:
                case = case.replace(var, str(variable_dict.get(a)))

            # case = case.replace(var, str(variable_dict.get(a)))
    print("-解析变量成功-------------------case: %s" %case)
    return case


def parse_func(case):
    print("---------------开始解析函数-------------------")
    # funcs = re.findall(r"\$\{\w+\(+.*?\)+.*?\}", case)
    funcs = re.findall(r"\$\{\w+\(+.*?\)\}", case)
    if len(funcs) > 0:
        print("需解析函数------------funcs: %s" %funcs)
        for func in funcs:
            a = func.lstrip("${").rstrip("}")
            # print(eval(a))
            case = case.replace(func, str(eval(a)))
    print("解析函数成功------------case: %s" % case)
    return case


def parse_case(variable_dict, case):
    case = parse_variable(variable_dict, case)
    case = parse_func(case)
    print("解析完成-------------case:%s" %case)
    return case


if __name__ == '__main__':
    # case1 = "{'host': '192.168.18.37:8097', 'http_type': 'http', 'timeout': 10, 'case_name': '7050login', 'case_url': '/ajaxLogin', 'case_method': 'POST', 'case_headers': {'Content-Type': 'application/json'}, 'case_json': {'username': 'admin', 'password': 'e10adc3949ba59abbe56e057f20f883e', 'isRememberPwd': 'false'}, 'case_file': None, 'case_validate': {'status_code': 200, 'headers.Content-Type': 'application/json;charset=UTF-8', 'content.code': '000', 'content.data.username': 'admin'}, 'case_extract': {'rspcode': 'content.code', 'username': 'content.data.username', 'token': 'content.data.sessionId'}, 'setup_hooks': [], 'teardown_hooks': []}"
    # print(case1)
    # field_check(exp_dict, response)
    # parseVariable(testcase)
    # parseFunc(testcase1)
    import json
    case = "{'timeout': 10, 'http_type': 'http', 'host': 'gateway.baolvtest.paas.com', 'case_id': 12,'case_name': '获取用户信息-admin', 'case_variable': {}, 'case_cookie': None,'case_url': '/gateway/api-ms/system/users/info', 'case_method': 'GET', 'case_headers': {'Content - Type': 'application / json', 'token': '{'content.access_token': None}'}, 'case_json': {}, 'case_file': None, 'case_validate': {'content.resultCode': '0'}, 'case_extract': {'resultCode': 'content.resultCode'}, 'setup_hooks': [], 'teardown_hooks': []}"
    # parse_variable(variable_dict, case)
    print(type(case))
    print(case)
    case1 = json.loads(case)
    # case1 = eval(case)
    print(type(case1))
    print(case1)
