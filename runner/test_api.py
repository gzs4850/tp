#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 15:18
# @Author  : z.g

import pytest
from bin import api_exec
# pip install -i https://pypi.doubanio.com/simple/ pymysql

# testsuit = '[[{"case":{"name":"管理员登录","request":{"variable":{"username":"admin"},"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"${username}","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":{"rspcode":"content.code","username":"content.data.username","token":"content.data.sessionId"},"validate":{"status_code":200,"headers.Content-Type":"application/json;charset=UTF-8","content.code":"000","content.data.username":"admin"},"setup_hooks":[],"teardown_hooks":[]}}}],[{"case":{"name":"登录","request":{"variable":{},"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":{"rspcode":"content.code","username":"content.data.username","token":"content.data.sessionId"},"validate":{"status_code":200,"headers.Content-Type":"application/json;charset=UTF-8","content.code":"000","content.data.username":"admin"},"setup_hooks":[],"teardown_hooks":[]}}},{"case":{"name":"getUserInfo","request":{"variable":{},"cookie":"Y","url":"/zlstBigData/permission/user/getUserInfo","method":"GET","headers":{},"json":{},"extract":[],"validate":{"status_code":200,"headers.Content-Type":"application/json","content.code":"000"},"setup_hooks":[],"teardown_hooks":[]}}}]]'


class TestApi:
    def test_api(self):
        testsuit = '[[{"case":{"name":"管理员登录","request":{"variable":{"username":"admin"},"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"${username}","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":{"rspcode":"content.code","username":"content.data.username","token":"content.data.sessionId"},"validate":{"status_code":200,"headers.Content-Type":"application/json;charset=UTF-8","content.code":"000","content.data.username":"admin"},"setup_hooks":[],"teardown_hooks":[]}}}],[{"case":{"name":"登录","request":{"variable":{},"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":{"rspcode":"content.code","username":"content.data.username","token":"content.data.sessionId"},"validate":{"status_code":200,"headers.Content-Type":"application/json;charset=UTF-8","content.code":"000","content.data.username":"admin"},"setup_hooks":[],"teardown_hooks":[]}}},{"case":{"name":"getUserInfo","request":{"variable":{},"cookie":"Y","url":"/zlstBigData/permission/user/getUserInfo","method":"GET","headers":{},"json":{},"extract":[],"validate":{"status_code":200,"headers.Content-Type":"application/json","content.code":"000"},"setup_hooks":[],"teardown_hooks":[]}}}]]'

        api_exec.exec_api(testsuit)

if __name__ == '__main__':
     pytest.main()