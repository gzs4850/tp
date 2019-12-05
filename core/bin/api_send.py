#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 15:37
# @Author  : z.g

import allure
import json
from core.bin import api_method, cookie_oper, log

Logger = log.Log()

def send_request(case_dict):
    """
    封装请求
    :param data: 测试用例
    :param host: 测试host
    :param address: 接口地址
    :param relevance: 关联对象
    :param _path: case路径
    :return:
    """
    Logger.info("="*100)
    headers = case_dict["case_headers"]
    if case_dict.get("case_cookie") == 'Y':
        headers["Cookie"] = cookie_oper.get_cookie()
    Logger.debug("请求头处理结果：%s" % headers)

    # print("请求头处理结果：%s" % headers)
    if case_dict["case_file"] is not None:
        parameter = case_dict["case_file"]
        # print("请求参数处理结果：%s" % case_dict["case_file"])
    else:
        parameter = json.dumps(case_dict["case_json"])
        # print("请求参数处理结果：%s" % case_dict["case_json"])
    Logger.debug("请求参数处理结果：%s" % parameter)

    host = case_dict["host"]
    Logger.debug("host处理结果： %s" % host)

    Logger.info("请求接口：%s" % str(case_dict["case_name"]))
    Logger.info("请求地址：%s" % case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
    Logger.info("请求头: %s" % str(headers))
    Logger.info("请求参数: %s" % str(parameter))

    if case_dict["case_name"] == '登录':
        with allure.step("保存cookie信息"):
            allure.attach("请求接口：", str(case_dict["case_name"]))
            allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
            allure.attach("请求头", str(headers))
            allure.attach("请求参数", str(parameter))
            api_method.save_cookie(header=headers, address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"], data=parameter)

    if case_dict["case_method"].lower() == 'post':
        Logger.info("请求方法: POST")
        if case_dict["case_file"]:
            with allure.step("POST上传文件"):
                allure.attach("请求接口：",str(case_dict["case_name"]))
                allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
                allure.attach("请求头", str(headers))
                allure.attach("请求参数", str(parameter))

            result = api_method.post(header=headers,
                                     address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                     request_parameter_type=case_dict["case_headers"]["Content-Type"],
                                     files=parameter,
                                     timeout=case_dict["timeout"])
        else:
            with allure.step("POST请求接口"):
                allure.attach("请求接口：", str(case_dict["case_name"]))
                allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
                allure.attach("请求头", str(headers))
                allure.attach("请求参数", str(parameter))

            result = api_method.post(header=headers,
                                     address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                     request_parameter_type=case_dict["case_headers"]["Content-Type"],
                                     data=parameter,
                                     timeout=case_dict["timeout"])

    elif case_dict["case_method"].lower() == 'get':
        with allure.step("GET请求接口"):
            allure.attach("请求接口：", str(case_dict["case_name"]))
            allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
            allure.attach("请求头", str(headers))
            allure.attach("请求参数", str(parameter))
            Logger.info("请求方法: GET")
        result = api_method.get(header=headers,
                                address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                data=parameter,
                                timeout=case_dict["timeout"])

    elif case_dict["case_method"].lower() == 'put':
        Logger.info("请求方法: PUT")
        if case_dict["case_file"]:
            with allure.step("PUT上传文件"):
                allure.attach("请求接口：", str(case_dict["case_name"]))
                allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
                allure.attach("请求头", str(headers))
                allure.attach("请求参数", str(parameter))
            result = api_method.post(header=headers,
                                     address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                     request_parameter_type=case_dict["case_headers"]["Content-Type"],
                                     files=parameter,
                                     timeout=case_dict["timeout"])

        else:
            with allure.step("PUT请求接口"):
                allure.attach("请求接口：", str(case_dict["case_name"]))
                allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
                allure.attach("请求头", str(headers))
                allure.attach("请求参数", str(parameter))
            result = api_method.post(header=headers,
                                     address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                     request_parameter_type=case_dict["case_headers"]["Content-Type"],
                                     data=parameter,
                                     timeout=case_dict["timeout"])

    elif case_dict["case_method"].lower() == 'delete':
        with allure.step("DELETE请求接口"):
            allure.attach("请求接口：", str(case_dict["case_name"]))
            allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
            allure.attach("请求头", str(headers))
            allure.attach("请求参数", str(parameter))
        Logger.info("请求方法: DELETE")
        result = api_method.get(header=headers,
                                address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                data=parameter,
                                timeout=case_dict["timeout"])
    else:
        result = {"code": False, "data": False}
    Logger.info("请求接口结果：\n %s" % str(result))
    return result


if __name__ == '__main__':
    testcase = "[{'host': '192.168.18.37:8097', 'http_type': 'http', 'timeout': 10, 'case_name': '7050login', 'case_url': '/ajaxLogin', 'case_method': 'POST', 'case_headers': {'Content-Type': 'application/json'}, 'case_json': {'username': 'admin', 'password': 'e10adc3949ba59abbe56e057f20f883e', 'isRememberPwd': 'false'}, 'case_file': None, 'case_validate': [{'eq': ['status_code', 200]}, {'eq': ['headers.Content-Type', 'application/json']}, {'eq': ['content.code', '000']}], 'case_extract': [{'token': 'content.data.sessionId'}], 'setup_hooks': [], 'teardown_hooks': []}, {'host': '192.168.18.37:8097', 'http_type': 'http', 'timeout': 10, 'case_name': 'getUserInfo', 'case_url': '/zlstBigData/permission/user/getUserInfo', 'case_method': 'GET', 'case_headers': {}, 'case_json': {}, 'case_file': None, 'case_validate': [{'eq': ['status_code', 200]}, {'eq': ['headers.Content-Type', 'application/json']}, {'eq': ['content.code', '000']}], 'case_extract': [], 'setup_hooks': [], 'teardown_hooks': []}, {'host': '192.168.18.37:8097', 'http_type': 'http', 'timeout': 10, 'case_name': 'getUserInfo', 'case_url': '/zlstBigData/permission/user/getUserInfo', 'case_method': 'GET', 'case_headers': {}, 'case_json': {}, 'case_file': None, 'case_validate': [{'eq': ['status_code', 200]}, {'eq': ['headers.Content-Type', 'application/json']}, {'eq': ['content.code', '000']}], 'case_extract': [], 'setup_hooks': [], 'teardown_hooks': []}]"
    testcase = eval(testcase)
    for case in testcase:
        print(case)
        result = send_request(case)
        print(result)