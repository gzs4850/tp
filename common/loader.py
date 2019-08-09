#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/1 14:31
# @Author  : z.g
import json
from common import readConfig

def load_testcase(testcase):

    host = readConfig.get_conf("ENV", "host")
    http_type = readConfig.get_conf("ENV", "http_type")
    timeout = readConfig.get_conf("ENV", "timeout")
    variable_dict = {}

    testcase = json.loads(testcase)
    testcase = testcase.get("testcase")
    print(testcase)

    for case in testcase:
        # print(case)

        case_dict = {}
        # if isinstance(testcase,str):
        #     testcase = json.loads(testcase)
        #     # print(testcase)

        case_dict["host"] = host
        case_dict["http_type"] = http_type
        case_dict["timeout"] = int(timeout)

        case_request = case.get("request")
        case_dict["case_name"] = case.get("name")
        case_dict["content_type"] = case.get("content_type")
        case_dict["case_validate"] = case.get("validate")
        case_dict["case_extract"] = case.get("extract")
        case_dict["case_url"] = case_request.get("url")
        case_dict["case_headers"] = case_request.get("headers")
        case_dict["case_method"] = case_request.get("method")
        case_dict["case_json"] = case_request.get("json")
        case_dict["case_file"] = case_request.get("file")

        variable_dict.update(case_dict["case_validate"])
        print("variable_dict:%s" % variable_dict)
        print("case_dict:%s" %case_dict)

    return case_dict,variable_dict


if __name__ == '__main__':
    testcase1 = '{"request": {"url": "/gateway/api-ms/system/users/info", "method": "POST", "content_type": "json","json": {"staffId": "2c94c234639f60b101639f8614b10029", "userCode": "17010101", "effectiveStarttime": "", "effectiveEndtime": ""}}, "name": "新增用户", "validate": [{"comparator": "equals", "check": "resultCode", "expected": 0}]}'
    testcase = '{"testcase":[{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": {"code": "000"}},{"request": {"url": "/zlstBigData/permission/user/getUserInfo","method": "GET", "json": {}}, "name": "获取用户信息", "content_type": "application/json", "validate": {"code": "000","data.orgName":"中铝集团"}}]}'
# testcase2 = '{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "123456", "validate": [{"comparator": "equals", "check": "code", "expected": "000"}]}'
    print(load_testcase(testcase))