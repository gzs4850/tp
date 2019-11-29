#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/29 16:42
# @Author  : z.g

from bin import case_load, config_parse, api_send
import json

def load_case(testsuit):
    host = config_parse.get_config("ENV", "host")
    http_type = config_parse.get_config("ENV", "http_type")
    timeout = config_parse.get_config("ENV", "timeout")
    testsuit = json.loads(testsuit)
    case_list = []
    for case in testsuit:
        case_dict = {}
        variable_dict = []
        case_dict["host"] = host
        case_dict["http_type"] = http_type
        case_dict["timeout"] = int(timeout)

        for step in case:
            print(step)
            step_detail = step.get("case")
            case_dict["case_name"] = step_detail.get("name")
            step_request = step_detail.get("request")
            case_dict["case_url"] = step_request.get("url")
            case_dict["case_method"] = step_request.get("method")
            case_dict["case_headers"] = step_request.get("headers")
            case_dict["case_json"] = step_request.get("json")
            case_dict["case_file"] = step_request.get("file")
            case_dict["case_validate"] = step_request.get("validate")
            case_dict["case_extract"] = step_request.get("extract")
            case_dict["setup_hooks"] = step_request.get("setup_hooks")
            case_dict["teardown_hooks"] = step_request.get("teardown_hooks")
            case_list.append(case_dict)
            variable_dict.append(case_dict["case_extract"])
    return case_list

def exec_api(testsuit):
    case_list = load_case(testsuit)
    for case in case_list:
        code, result = api_send.send_request(case)
        print(code, result)

    return code, result


if __name__ == '__main__':
    testsuit = '[[{"case":{"name":"7050login","request":{"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":[{"token":"content.data.sessionId"}],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.code","000"]}],"setup_hooks":[],"teardown_hooks":[]}}}],[{"case":{"name":"7050login","request":{"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":[{"token":"content.data.sessionId"}],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.code","000"]}],"setup_hooks":[],"teardown_hooks":[]}}},{"case":{"name":"getUserInfo","request":{"url":"/zlstBigData/permission/user/getUserInfo","method":"GET","headers":{},"json":{},"extract":[],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.code","000"]}],"setup_hooks":[],"teardown_hooks":[]}}}]]'
    exec_api(testsuit)