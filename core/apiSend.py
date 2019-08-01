#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/1 11:10
# @Author  : z.g

from common import logger
from core import apiMethod
from common import loader

def send_request(testcase):

    case_dict = loader.load_testcase(testcase)
    logger.log_info("*" * 100)
    headers = case_dict["headers"]

    logger.log_debug("请求头处理结果：%s" % headers)
    if case_dict["file"] is not None:
        parameter = case_dict["case_file"]
        logger.log_debug("请求参数处理结果：%s" % case_dict["case_file"])
    else:
        parameter = case_dict["case_json"]
        logger.log_debug("请求参数处理结果：%s" % case_dict["case_json"])

    try:
        host = case_dict["host"]
    except KeyError:
        pass
    try:
        url = case_dict["url"]
    except KeyError:
        pass

    logger.log_debug("host处理结果： %s" % host)
    if not host:
        raise Exception("接口请求地址为空 %s" % case_dict["host"])
    logger.log_info("请求接口：%s" % str(case_dict["case_name"]))
    logger.log_info("请求地址：%s" % case_dict["http_type"] + "://" + host + url)
    logger.log_info("请求头: %s" % str(headers))
    logger.log_info("请求参数: %s" % str(parameter))
    # if data["test_name"] == 'password正确':
    #     with allure.step("保存cookie信息"):
    #         allure.attach("请求接口：", str(data["test_name"]))
    #         allure.attach("请求地址", data["http_type"] + "://" + host + address)
    #         allure.attach("请求头", str(header))
    #         allure.attach("请求参数", str(parameter))
    #         apiMethod.save_cookie(header=header, address=data["http_type"] + "://" + host + address, data=parameter)

    if case_dict["case_method"].lower() == 'post':
        logger.log_info("请求方法: POST")
        if case_dict["case_file"]:
            # with allure.step("POST上传文件"):
            #     allure.attach("请求接口：",str(data["test_name"]))
            #     allure.attach("请求地址", data["http_type"] + "://" + host + address)
            #     allure.attach("请求头", str(header))
            #     allure.attach("请求参数", str(parameter))

            result = apiMethod.post(header=headers,
                                    address=case_dict["http_type"] + "://" + host + url,
                                    request_parameter_type=case_dict["parameter_type"],
                                    files=parameter,
                                    timeout=case_dict["timeout"])
        else:
            # with allure.step("POST请求接口"):
            #     allure.attach("请求接口：", str(data["test_name"]))
            #     allure.attach("请求地址", data["http_type"] + "://" + host + address)
            #     allure.attach("请求头", str(header))
            #     allure.attach("请求参数", str(parameter))
            result = apiMethod.post(header=headers,
                                    address=case_dict["http_type"] + "://" + host + url,
                                    request_parameter_type=case_dict["parameter_type"],
                                    data=parameter,
                                    timeout=case_dict["timeout"])
    elif case_dict["request_type"].lower() == 'get':
        # with allure.step("GET请求接口"):
        #     allure.attach("请求接口：", str(data["test_name"]))
        #     allure.attach("请求地址", data["http_type"] + "://" + host + address)
        #     allure.attach("请求头", str(header))
        #     allure.attach("请求参数", str(parameter))
        #     logging.info("请求方法: GET")
        result = apiMethod.get(header=headers,
                               address=case_dict["http_type"] + "://" + host + url,
                               data=parameter,
                               timeout=case_dict["timeout"])
    elif case_dict["request_type"].lower() == 'put':
        logger.log_info("请求方法: PUT")
        if case_dict["file"]:
            # with allure.step("PUT上传文件"):
            #     allure.attach("请求接口：",str(data["test_name"]))
            #     allure.attach("请求地址", data["http_type"] + "://" + host + address)
            #     allure.attach("请求头", str(header))
            #     allure.attach("请求参数", str(parameter))
            result = apiMethod.post(header=headers,
                                    address=case_dict["http_type"] + "://" + host + url,
                                    request_parameter_type=case_dict["parameter_type"],
                                    files=parameter,
                                    timeout=case_dict["timeout"])
        else:
            # with allure.step("PUT请求接口"):
            #     allure.attach("请求接口：", str(data["test_name"]))
            #     allure.attach("请求地址", data["http_type"] + "://" + host + address)
            #     allure.attach("请求头", str(header))
            #     allure.attach("请求参数", str(parameter))
            result = apiMethod.post(header=headers,
                                    address=case_dict["http_type"] + "://" + host + url,
                                    request_parameter_type=case_dict["parameter_type"],
                                    data=parameter,
                                    timeout=case_dict["timeout"])
    elif case_dict["request_type"].lower() == 'delete':
        # with allure.step("DELETE请求接口"):
        #     allure.attach("请求接口：", str(data["test_name"]))
        #     allure.attach("请求地址", data["http_type"] + "://" + host + address)
        #     allure.attach("请求头", str(header))
        #     allure.attach("请求参数", str(parameter))
        logger.log_info("请求方法: DELETE")
        result = apiMethod.get(header=headers,
                               address=case_dict["http_type"] + "://" + host + url,
                               data=parameter,
                               timeout=case_dict["timeout"])
    else:
        result = {"code": False, "data": False}
    logger.log_info("请求接口结果：\n %s" % str(result))
    return result

testcase = '{"request": {"url": "/ajaxLogin", "content_type": "json","headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "validate": [{"comparator": "equals", "check": "code", "expected": "000"}]}'

send_request(testcase)
