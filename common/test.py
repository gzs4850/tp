#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/1 17:28
# @Author  : z.g

from common import logger
from core import apiMethod
from common import loader
import json
import logging

def send_request(testcase):
    case_dict = loader.load_testcase(testcase)
    print(case_dict)
    print("*" * 100)

    headers = case_dict["case_headers"]

    print("请求头处理结果：%s" % headers)
    if case_dict["case_file"] is not None:
        parameter = case_dict["case_file"]
        print("请求参数处理结果：%s" % case_dict["case_file"])
    else:
        parameter = json.dumps(case_dict["case_json"])
        print("请求参数处理结果：%s" % case_dict["case_json"])

    print("host地址：%s" % case_dict["host"])
    print("请求接口：%s" % str(case_dict["case_name"]))
    print("请求地址：%s" % case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
    print("请求头: %s" % str(headers))
    print("请求参数: %s" % str(parameter))

    if case_dict["case_method"].lower() == 'post':
        print("请求方法: POST")
        if case_dict["case_file"]:
            result = apiMethod.post(header=headers,
                                    address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                    request_parameter_type=case_dict["content_type"],
                                    files=parameter,
                                    timeout=case_dict["timeout"])
        else:
            result = apiMethod.post(header=headers,
                                    address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                    request_parameter_type=case_dict["content_type"],
                                    data=parameter,
                                    timeout=case_dict["timeout"])
    elif case_dict["request_type"].lower() == 'get':
        result = apiMethod.get(header=headers,
                               address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                               data=parameter,
                               timeout=case_dict["timeout"])
    elif case_dict["request_type"].lower() == 'put':
        if case_dict["case_file"]:
            result = apiMethod.post(header=headers,
                                    address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                    request_parameter_type=case_dict["content_type"],
                                    files=parameter,
                                    timeout=case_dict["timeout"])
        else:
            result = apiMethod.post(header=headers,
                                    address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                    request_parameter_type=case_dict["content_type"],
                                    data=parameter,
                                    timeout=case_dict["timeout"])
    elif case_dict["request_type"].lower() == 'delete':
        result = apiMethod.get(header=headers,
                               address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                               data=parameter,
                               timeout=case_dict["timeout"])
    else:
        result = {"code": False, "data": False}
    print("请求接口结果：\n %s" % str(result))
    print(type(result))
    return result

testcase = '{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": [{"comparator": "equals", "check": "code", "expected": "000"}]}'

send_request(testcase)