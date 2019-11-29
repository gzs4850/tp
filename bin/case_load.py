#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 17:16
# @Author  : z.g

import json
from bin import config_parse
from bin import case_parse
# from common import readConfig


def load(testsuit):

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


if __name__ == '__main__':
    testsuit = '[[{"case":{"name":"7050login","request":{"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":[{"token":"content.data.sessionId"}],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.code","000"]}],"setup_hooks":[],"teardown_hooks":[]}}}],[{"case":{"name":"7050login","request":{"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":"false"},"extract":[{"token":"content.data.sessionId"}],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.code","000"]}],"setup_hooks":[],"teardown_hooks":[]}}},{"case":{"name":"getUserInfo","request":{"url":"/zlstBigData/permission/user/getUserInfo","method":"GET","headers":{},"json":{},"extract":[],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.code","000"]}],"setup_hooks":[],"teardown_hooks":[]}}}]]'
    # testsuit = '[[{"case":{"name":"7050login","request":{"url":"/ajaxLogin","method":"POST","headers":{"Content-Type": "application/json"},"json":{"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}},"extract":[{"token":"content.data.sessionId"}],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.code","000"]}],"setup_hooks":[],"teardown_hooks":[]}}}],[{{"eq":["content.code","000"]}},{"case":{"name":"getUserInfo","request":{"url":"/zlstBigData/permission/user/getUserInfo","method":"GET","headers":{},"json":{},"extract":[],"validate":[{"eq":["status_code",200]},{{"eq":["content.code","000"]}],"setup_hooks":[],"teardown_hooks":[]}}}]]'
    # testsuit1 = '{"request": {"url": "/gateway/api-ms/system/users/info", "method": "POST", "content_type": "json","json": {"staffId": "2c94c234639f60b101639f8614b10029", "userCode": "17010101", "effectiveStarttime": "", "effectiveEndtime": ""}}, "name": "新增用户", "validate": [{"comparator": "equals", "check": "resultCode", "expected": 0}]}'
    # testsuit = '{"testcase":[{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": {"code": "000"}},{"request": {"url": "/zlstBigData/permission/user/getUserInfo","method": "GET", "json": {}}, "name": "获取用户信息", "content_type": "application/json", "validate": {"code": "000","data.orgName":"中铝集团"}}]}'
# testcase2 = '{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "123456", "validate": [{"comparator": "equals", "check": "code", "expected": "000"}]}'
    print(load(testsuit))

"""
[[{"case":{"name":"gettokenwith$user_agent,$os_platform,$app_version","request":{"url":"/api/get-token","method":"POST","headers":{"app_version":"$app_version","os_platform":"$os_platform","user_agent":"$user_agent"},"json":{"sign":"${get_sign($user_agent,$device_sn,$os_platform,$app_version)}"},"extract":[{"token":"content.token"}],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.success",true]}],"setup_hooks":[],"teardown_hooks":[]}}}],[{"case":{"name":"gettokenwith$user_agent,$os_platform,$app_version","request":{"url":"/api/get-token","method":"POST","headers":{"app_version":"$app_version","os_platform":"$os_platform","user_agent":"$user_agent"},"json":{"sign":"${get_sign($user_agent,$device_sn,$os_platform,$app_version)}"},"extract":[{"token":"content.token"}],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.success",true]}],"setup_hooks":[],"teardown_hooks":[]}}},{"case":{"name":"gettokenwith$user_agent,$os_platform,$app_version","request":{"url":"/api/get-token","method":"POST","headers":{"app_version":"$app_version","os_platform":"$os_platform","user_agent":"$user_agent"},"json":{"sign":"${get_sign($user_agent,$device_sn,$os_platform,$app_version)}"},"extract":[{"token":"content.token"}],"validate":[{"eq":["status_code",200]},{"eq":["headers.Content-Type","application/json"]},{"eq":["content.success",true]}],"setup_hooks":[],"teardown_hooks":[]}}}]]
"""

"""
testsuit:
    
[
    [
        {
            "case":{
                "name":"7050login",
                "request":{
                    "url":"/ajaxLogin",
                    "method":"POST",
                    "headers":{
                        "Content-Type":"application/json"
                    },
                    "json":{
                        "username":"admin",
                        "password":"e10adc3949ba59abbe56e057f20f883e",
                        "isRememberPwd":false
                    },
                    "extract":[
                        {
                            "token":"content.data.sessionId"
                        }
                    ],
                    "validate":[
                        {
                            "eq":[
                                "status_code",
                                200
                            ]
                        },
                        {
                            "eq":[
                                "headers.Content-Type",
                                "application/json"
                            ]
                        },
                        {
                            "eq":[
                                "content.code",
                                "000"
                            ]
                        }
                    ],
                    "setup_hooks":[

                    ],
                    "teardown_hooks":[

                    ]
                }
            }
        }
    ],
    [
        {
            "case":{
                "name":"7050login",
                "request":{
                    "url":"/ajaxLogin",
                    "method":"POST",
                    "headers":{
                        "Content-Type":"application/json"
                    },
                    "json":{
                        "username":"admin",
                        "password":"e10adc3949ba59abbe56e057f20f883e",
                        "isRememberPwd":false
                    },
                    "extract":[
                        {
                            "token":"content.data.sessionId"
                        }
                    ],
                    "validate":[
                        {
                            "eq":[
                                "status_code",
                                200
                            ]
                        },
                        {
                            "eq":[
                                "headers.Content-Type",
                                "application/json"
                            ]
                        },
                        {
                            "eq":[
                                "content.code",
                                "000"
                            ]
                        }
                    ],
                    "setup_hooks":[

                    ],
                    "teardown_hooks":[

                    ]
                }
            }
        },
        {
            "case":{
                "name":"getUserInfo",
                "request":{
                    "url":"/zlstBigData/permission/user/getUserInfo",
                    "method":"GET",
                    "headers":{

                    },
                    "json":{

                    },
                    "extract":[

                    ],
                    "validate":[
                        {
                            "eq":[
                                "status_code",
                                200
                            ]
                        },
                        {
                            "eq":[
                                "headers.Content-Type",
                                "application/json"
                            ]
                        },
                        {
                            "eq":[
                                "content.code",
                                "000"
                            ]
                        }
                    ],
                    "setup_hooks":[

                    ],
                    "teardown_hooks":[

                    ]
                }
            }
        }
    ]
]
    
"""