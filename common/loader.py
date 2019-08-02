#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/1 14:31
# @Author  : z.g
import json

def load_testcase(testcase):
    from common import readConfig
    host = readConfig.get_conf("ENV", "host")
    http_type = readConfig.get_conf("ENV", "http_type")
    timeout = readConfig.get_conf("ENV", "timeout")

    case_dict = {}
    if isinstance(testcase,str):
        testcase = json.loads(testcase)

    case_dict["host"] = host
    case_dict["http_type"] = http_type
    case_dict["timeout"] = int(timeout)

    case_request = testcase.get("request")
    case_dict["case_name"] = testcase.get("name")
    case_dict["content_type"] = testcase.get("content_type")
    case_dict["case_validate"] = testcase.get("validate")
    case_dict["case_extract"] = testcase.get("extract")
    case_dict["case_url"] = case_request.get("url")
    case_dict["case_headers"] = case_request.get("headers")
    case_dict["case_method"] = case_request.get("method")
    case_dict["case_json"] = case_request.get("json")
    case_dict["case_file"] = case_request.get("file")
    # print(case_dict)
    return case_dict

# testcase1 = '{"request": {"url": "/gateway/api-ms/system/users/info", "method": "POST", "content_type": "json","json": {"staffId": "2c94c234639f60b101639f8614b10029", "userCode": "17010101", "effectiveStarttime": "", "effectiveEndtime": ""}}, "name": "新增用户", "validate": [{"comparator": "equals", "check": "resultCode", "expected": 0}]}'

# testcase2 = '{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "123456", "validate": [{"comparator": "equals", "check": "code", "expected": "000"}]}'
#
# load_testcase(testcase2)