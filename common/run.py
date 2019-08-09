#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/9 16:32
# @Author  : z.g

import json
from common import loader
from common import parse
from core import apiSend



if __name__ == '__main__':
    testcase = '{"testcase":[{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": {"code": "000"}},{"request": {"url": "/zlstBigData/permission/user/getUserInfo","method": "GET", "json": {}}, "name": "获取用户信息", "content_type": "application/json", "validate": {"code": "000","data.orgName":"中铝集团"}}]}'
    testcase2 = '{"request": {"url": "/zlstBigData/permission/user/getUserInfo","method": "GET", "json": {}}, "name": "获取用户信息", "content_type": "application/json", "validate": {"code": "000","data.orgName":"中铝集团"}}'
    testcases = json.loads(testcase)
    for testcase in testcases.get("testcase"):
        case_dict = loader.load_testcase(testcase)
        result = apiSend.send_request(case_dict)
        parse.field_check(case_dict, result)