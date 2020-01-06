#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/29 16:42
# @Author  : z.g
from pymysql import escape_string

from core.bin import config_parse, api_send, result_check, field_extract, case_parse, log, mysql_oper
import json
import time

mc = mysql_oper.MysqlConnect()
Logger = log.Log()

def load_case(testsuit):
    # print("testsuit: %s" % testsuit)
    # host = config_parse.get_config("ENV", "host")
    # http_type = config_parse.get_config("ENV", "http_type")
    timeout = config_parse.get_config("ENV", "timeout")
    testsuit = json.loads(testsuit)
    case_list = []
    for case in testsuit:
        step_list = []
        for step in case:
            # print("step: %s" %step)
            case_dict = {}
            case_dict["timeout"] = int(timeout)
            step_detail = step.get("case")
            baseurl = step_detail.get("baseurl")
            case_dict["http_type"] = baseurl.split('://', 1)[0]
            case_dict["host"] = baseurl.split('://', 1)[1]
            case_dict["case_id"] = step_detail.get("id")
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

def exec_api(testsuit, pch):
    case_list = load_case(testsuit)
    print("case_list:%s" % case_list)
    for step in case_list:
        variable_dict = {}
        for case in step:
            print("---------case:%s" % case)
            case_id = case.get("case_id")
            print("case_id:%s" % case_id)
            variable_dict.update(case.get("case_variable"))
            print("第一次打印： %s" %variable_dict)

            # 字典转字符串str(dict)
            # 字符串转字典 eval(str)
            case1 = case_parse.parse_case(variable_dict, str(case))
            print("解析成功-----------case1: %s" % case1)
            print("解析成功-----------type of case1: %s" % type(case1))
            case = eval(case1)
            print("解析成功-----------case: %s" % case)

            # case = eval(case_parse.parse_case(variable_dict, str(case)))
            # print("解析成功-----------case: %s" %case)

            start_time = time.strftime("%Y-%m-%d %X",time.localtime())
            # 发送请求，返回code，response, headers
            response = api_send.send_request(case)
            # print(response)

            code = response[0]
            result = response[1]
            headers = response[2]
            elapsedtime = response[3]
            req_data = response[4]
            req_header = response[5]
            req_url = response[6]

            # code, result, headers, elapsedtime, req_data, req_header= api_send.send_request(case)
            # 测试结果持久化
            Logger.info("用例 %s 请求URL： %s" % (case.get("case_name"), req_url))
            Logger.info("用例 %s 请求头： %s" % (case.get("case_name"), req_header))
            Logger.info("用例 %s 请求体： \n %s" % (case.get("case_name"), req_data))
            Logger.info("用例 %s 响应状态码： %s" % (case.get("case_name"), code))
            Logger.info("用例 %s 响应头： %s" % (case.get("case_name"), headers))
            Logger.info("用例 %s 响应体： \n %s" % (case.get("case_name"), result))
            Logger.info("用例 %s 响应时长： %s" % (case.get("case_name"), elapsedtime))

            # print(code, result, headers, elapsedtime, req_data, req_header)

            # 结果集验证
            # print(result_check.check(case, code, result, headers))
            if result_check.check(case, code, result, headers)[0]:
                test_result = "pass"
                Logger.info("用例 %s 测试通过" %case.get("case_name"))
                # print("用例 %s 测试通过" %case.get("case_name"))
            else:
                test_result = "fail"
                Logger.error("用例 %s 测试失败" % case.get("case_name"))
                # print("用例 %s 测试失败" % case.get("case_name"))

            assert_msg = result_check.check(case, code, result, headers)[1]

            if isinstance(req_data, str):
                req_data = json.loads(req_data)

            print(type(result))
            if isinstance(result, str):
                result = json.loads(result)
            #
            # if len(assert_msg) > 0:
            #     msgInfo = []
            #     for msg in assert_msg:
            #         msgInfo.append(escape_string(msg))

            mc.exec_data('insert into testresults(case_id, test_result, real_rsp_code, real_req_path, real_req_head, real_req_json, real_rsp_head, real_rsp_json, real_rsp_time, assert_msg, timestamp, batch_number) '
                         'values(%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
                         %(case_id, test_result, code, req_url, req_header, req_data, headers, result, elapsedtime, assert_msg, start_time, pch))

            # 从响应体、响应头中提取字段值
            variable_dict.update(field_extract.extract(case, result, headers))
            print('variable_dict: %s' %variable_dict)

        # return code, result, headers


if __name__ == '__main__':
    testsuit = '[[{"case":{"name":"管理员登录","request":{"variable":{"username":"admin"},"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"${username}","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":{"rspcode":"content.code","username":"content.data.username","token":"content.data.sessionId"},"validate":{"status_code":200,"headers.Content-Type":"application/json;charset=UTF-8","content.code":"000","content.data.username":"admin"},"setup_hooks":[],"teardown_hooks":[]}}}],[{"case":{"name":"登录","request":{"variable":{},"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":{"rspcode":"content.code","username":"content.data.username","token":"content.data.sessionId"},"validate":{"status_code":200,"headers.Content-Type":"application/json;charset=UTF-8","content.code":"000","content.data.username":"admin"},"setup_hooks":[],"teardown_hooks":[]}}},{"case":{"name":"getUserInfo","request":{"variable":{},"cookie":"Y","url":"/zlstBigData/permission/user/getUserInfo","method":"GET","headers":{},"json":{},"extract":[],"validate":{"status_code":200,"headers.Content-Type":"application/json","content.code":"000"},"setup_hooks":[],"teardown_hooks":[]}}}]]'
    exec_api(testsuit)
