#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 15:37
# @Author  : z.g

import logging
import allure
import json
from . import api_method, case_load, case_parse
# from bin.unit import apiMethod, replaceRelevance
# from bin.unit import initializeCookie
# from bin.config import confManage
# from bin.unit import readParameter


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
    logging.info("="*100)
    headers = case_dict["case_headers"]
    logging.debug("请求头处理结果：%s" % headers)

    # print("请求头处理结果：%s" % headers)
    if case_dict["case_file"] is not None:
        parameter = case_dict["case_file"]
        # print("请求参数处理结果：%s" % case_dict["case_file"])
    else:
        parameter = json.dumps(case_dict["case_json"])
        # print("请求参数处理结果：%s" % case_dict["case_json"])
    logging.debug("请求参数处理结果：%s" % parameter)

    host = case_dict["host"]
    logging.debug("host处理结果： %s" % host)

    logging.info("请求接口：%s" % str(case_dict["name"]))
    logging.info("请求地址：%s" % case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
    logging.info("请求头: %s" % str(headers))
    logging.info("请求参数: %s" % str(parameter))

    if case_dict["case_method"].lower() == 'post':
        logging.info("请求方法: POST")
        if case_dict["case_file"]:
            with allure.step("POST上传文件"):
                allure.attach("请求接口：",str(case_dict["name"]))
                allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
                allure.attach("请求头", str(headers))
                allure.attach("请求参数", str(parameter))

            result = api_method.post(header=headers,
                                     address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                     request_parameter_type=case_dict["content_type"],
                                     files=parameter,
                                     timeout=case_dict["timeout"])
        else:
            with allure.step("POST请求接口"):
                allure.attach("请求接口：", str(case_dict["name"]))
                allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
                allure.attach("请求头", str(headers))
                allure.attach("请求参数", str(parameter))

            result = api_method.post(header=headers,
                                     address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                     request_parameter_type=case_dict["content_type"],
                                     data=parameter,
                                     timeout=case_dict["timeout"])

    elif case_dict["case_method"].lower() == 'get':
        with allure.step("GET请求接口"):
            allure.attach("请求接口：", str(case_dict["name"]))
            allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
            allure.attach("请求头", str(headers))
            allure.attach("请求参数", str(parameter))
            logging.info("请求方法: GET")
        result = api_method.get(header=headers,
                                address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                data=parameter,
                                timeout=case_dict["timeout"])

    elif case_dict["case_method"].lower() == 'put':
        logging.info("请求方法: PUT")
        if case_dict["case_file"]:
            with allure.step("PUT上传文件"):
                allure.attach("请求接口：", str(case_dict["name"]))
                allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
                allure.attach("请求头", str(headers))
                allure.attach("请求参数", str(parameter))
            result = api_method.post(header=headers,
                                     address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                     request_parameter_type=case_dict["content_type"],
                                     files=parameter,
                                     timeout=case_dict["timeout"])

        else:
            with allure.step("PUT请求接口"):
                allure.attach("请求接口：", str(case_dict["name"]))
                allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
                allure.attach("请求头", str(headers))
                allure.attach("请求参数", str(parameter))
            result = api_method.post(header=headers,
                                     address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                     request_parameter_type=case_dict["content_type"],
                                     data=parameter,
                                     timeout=case_dict["timeout"])

    elif case_dict["case_method"].lower() == 'delete':
        with allure.step("DELETE请求接口"):
            allure.attach("请求接口：", str(case_dict["name"]))
            allure.attach("请求地址", case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"])
            allure.attach("请求头", str(headers))
            allure.attach("请求参数", str(parameter))
        logging.info("请求方法: DELETE")
        result = api_method.get(header=headers,
                                address=case_dict["http_type"] + "://" + case_dict["host"] + case_dict["case_url"],
                                data=parameter,
                                timeout=case_dict["timeout"])
    else:
        result = {"code": False, "data": False}
    logging.info("请求接口结果：\n %s" % str(result))
    return result


if __name__ == '__main__':
    testcase = '{"testcase":[{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": {"code": "000"}},{"request": {"url": "/zlstBigData/permission/user/getUserInfo","method": "GET", "json": {}}, "name": "获取用户信息", "content_type": "application/json", "validate": {"code": "000","data.orgName":"中铝集团"}}]}'
    testcase2 = '{"request": {"url": "/zlstBigData/permission/user/getUserInfo","method": "GET", "json": {}}, "name": "获取用户信息", "content_type": "application/json", "validate": {"code": "000","data.orgName":"中铝集团"}}'
    testcases = json.loads(testcase)
    for testcase in testcases.get("testcase"):
        case_dict = case_load.load(testcase)
        result = send_request(case_dict)
        case_parse.field_check(case_dict, result)