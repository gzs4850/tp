#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/29 16:42
# @Author  : z.g

from bin import config_parse, api_send, result_check, field_extract, case_parse, log
import json

Logger = log.Log()

def load_case(testsuit):
    # print("testsuit: %s" % testsuit)
    host = config_parse.get_config("ENV", "host")
    http_type = config_parse.get_config("ENV", "http_type")
    timeout = config_parse.get_config("ENV", "timeout")
    testsuit = json.loads(testsuit)
    case_list = []
    for case in testsuit:
        step_list = []
        for step in case:
            case_dict = {}
            case_dict["host"] = host
            case_dict["http_type"] = http_type
            case_dict["timeout"] = int(timeout)
            step_detail = step.get("case")
            case_dict["case_name"] = step_detail.get("name")
            step_request = step_detail.get("request")
            case_dict["case_variable"] = step_request.get("variable")
            case_dict["case_cookie"] = step_request.get("cookie")
            case_dict["case_url"] = step_request.get("url")
            case_dict["case_method"] = step_request.get("method")
            case_dict["case_headers"] = step_request.get("headers")
            case_dict["case_json"] = step_request.get("json")
            case_dict["case_file"] = step_request.get("file")
            case_dict["case_validate"] = step_request.get("validate")
            case_dict["case_extract"] = step_request.get("extract")
            case_dict["setup_hooks"] = step_request.get("setup_hooks")
            case_dict["teardown_hooks"] = step_request.get("teardown_hooks")
            step_list.append(case_dict)
        case_list.append(step_list)
    # print("case_list: %s" % case_list)
    return case_list

def exec_api(testsuit):
    case_list = load_case(testsuit)
    # print("case_list:%s" % case_list)
    # variable_dict = {}
    for step in case_list:
        for case in step:
            # print("case:%s" % case)
            variable_dict = case.get("case_variable")

            # 字典转字符串str(dict)
            # 字符串转字典 eval(str)
            case = eval(case_parse.parse_case(variable_dict, str(case)))

            # 发送请求，返回code，response, headers
            response = api_send.send_request(case)
            # print(response)

            code = response[0]
            result = response[1]
            headers = response[2]
            elapsedtime = response[3]
            req_data = response[4]
            req_header = response[5]

            # code, result, headers, elapsedtime, req_data, req_header= api_send.send_request(case)
            # 测试结果持久化
            Logger.info("用例 %s 请求头： %s" % (case.get("case_name"), req_header))
            Logger.info("用例 %s 请求体： \n %s" % (case.get("case_name"), req_data))
            Logger.info("用例 %s 响应状态码： %s" % (case.get("case_name"), code))
            Logger.info("用例 %s 响应头： %s" % (case.get("case_name"), headers))
            Logger.info("用例 %s 响应体： \n %s" % (case.get("case_name"), result))
            Logger.info("用例 %s 响应时长： %s" % (case.get("case_name"), elapsedtime))

            # print(code, result, headers, elapsedtime, req_data, req_header)

            # 结果集验证
            if result_check.check(case, code, result, headers):
                Logger.info("用例 %s 测试通过" %case.get("case_name"))
                # print("用例 %s 测试通过" %case.get("case_name"))
            else:
                Logger.error("用例 %s 测试失败" % case.get("case_name"))
                # print("用例 %s 测试失败" % case.get("case_name"))

            # 从响应体、响应头中提取字段值
            variable_dict.update(field_extract.extract(case, result, headers))
            # print(variable_dict)

        # return code, result, headers


if __name__ == '__main__':
    testsuit = '[[{"case":{"name":"管理员登录","request":{"variable":{"username":"admin"},"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"${username}","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":{"rspcode":"content.code","username":"content.data.username","token":"content.data.sessionId"},"validate":{"status_code":200,"headers.Content-Type":"application/json;charset=UTF-8","content.code":"000","content.data.username":"admin"},"setup_hooks":[],"teardown_hooks":[]}}}],[{"case":{"name":"登录","request":{"variable":{},"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":{"rspcode":"content.code","username":"content.data.username","token":"content.data.sessionId"},"validate":{"status_code":200,"headers.Content-Type":"application/json;charset=UTF-8","content.code":"000","content.data.username":"admin"},"setup_hooks":[],"teardown_hooks":[]}}},{"case":{"name":"getUserInfo","request":{"variable":{},"cookie":"Y","url":"/zlstBigData/permission/user/getUserInfo","method":"GET","headers":{},"json":{},"extract":[],"validate":{"status_code":200,"headers.Content-Type":"application/json","content.code":"000"},"setup_hooks":[],"teardown_hooks":[]}}}]]'
    exec_api(testsuit)
