#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 15:18
# @Author  : z.g

import pytest
from bin import api_send

def getCase(testSuit):
    pass

class TestApi:
    def test_api(self, testcase):
        api_send(testcase)



if __name__ == '__main__':
    testsuit = '{"testcase":[{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": {"code": "000"}},{"request": {"url": "/zlstBigData/permission/user/getUserInfo","method": "GET", "json": {}}, "name": "获取用户信息", "content_type": "application/json", "validate": {"code": "000","data.orgName":"中铝集团"}}]}'
    testcase = '{"request": {"url": "/ajaxLogin", "content_type": "json","headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "validate": [{"comparator": "equals", "check": "code", "expected": "000"}]}'
    pytest.main("test_api.py")