#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 17:16
# @Author  : z.g

import json
from bin import config_parse
# from common import readConfig


def load(testsuit):
    host = config_parse.get_config("ENV", "host")
    http_type = config_parse.get_config("ENV", "http_type")
    timeout = config_parse.get_config("ENV", "timeout")
    variable_dict = {}

    testsuit = json.loads(testsuit)
    testsuit = testsuit.get("testcase")
    print(testsuit)

    for case in testsuit:
        # print(case)

        case_dict = {}
        # if isinstance(testsuit,str):
        #     testcase = json.loads(testsuit)
        #     # print(testcase)

        case_dict["host"] = host
        case_dict["http_type"] = http_type
        case_dict["timeout"] = int(timeout)

        case_request = case.get("request")
        case_dict["case_name"] = case.get("name")
        case_dict["content_type"] = case.get("content_type")
        case_dict["case_validate"] = case.get("validate")
        case_dict["case_extract"] = case.get("extract")
        case_dict["case_url"] = case_request.get("url")
        case_dict["case_headers"] = case_request.get("headers")
        case_dict["case_method"] = case_request.get("method")
        case_dict["case_json"] = case_request.get("json")
        case_dict["case_file"] = case_request.get("file")

        variable_dict.update(case_dict["case_validate"])
        print("variable_dict:%s" % variable_dict)
        print("case_dict:%s" %case_dict)

    return case_dict,variable_dict


if __name__ == '__main__':
    testsuit1 = '{"request": {"url": "/gateway/api-ms/system/users/info", "method": "POST", "content_type": "json","json": {"staffId": "2c94c234639f60b101639f8614b10029", "userCode": "17010101", "effectiveStarttime": "", "effectiveEndtime": ""}}, "name": "新增用户", "validate": [{"comparator": "equals", "check": "resultCode", "expected": 0}]}'
    testsuit = '{"testcase":[{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": {"code": "000"}},{"request": {"url": "/zlstBigData/permission/user/getUserInfo","method": "GET", "json": {}}, "name": "获取用户信息", "content_type": "application/json", "validate": {"code": "000","data.orgName":"中铝集团"}}]}'
# testcase2 = '{"request": {"url": "/ajaxLogin", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"admin","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "123456", "validate": [{"comparator": "equals", "check": "code", "expected": "000"}]}'
    print(load(testsuit))


"""

    testsuit:
    
    [[

    {
        "step":{
            "name":"get token with $user_agent, $os_platform, $app_version",
            "request":{
                "url":"/api/get-token",
                "method":"POST",
                "headers":{
                    "app_version":"$app_version",
                    "os_platform":"$os_platform",
                    "user_agent":"$user_agent"
                },
                "json":{
                    "sign":"${get_sign($user_agent, $device_sn, $os_platform, $app_version)}"
                },
                "extract":[
                    {
                        "token":"content.token"
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
                            "content.success",
                            true
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
        "step":{
            "name":"get token with $user_agent, $os_platform, $app_version",
            "request":{
                "url":"/api/get-token",
                "method":"POST",
                "headers":{
                    "app_version":"$app_version",
                    "os_platform":"$os_platform",
                    "user_agent":"$user_agent"
                },
                "json":{
                    "sign":"${get_sign($user_agent, $device_sn, $os_platform, $app_version)}"
                },
                "extract":[
                    {
                        "token":"content.token"
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
                            "content.success",
                            true
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
        "step":{
            "name":"get token with $user_agent, $os_platform, $app_version",
            "request":{
                "url":"/api/get-token",
                "method":"POST",
                "headers":{
                    "app_version":"$app_version",
                    "os_platform":"$os_platform",
                    "user_agent":"$user_agent"
                },
                "json":{
                    "sign":"${get_sign($user_agent, $device_sn, $os_platform, $app_version)}"
                },
                "extract":[
                    {
                        "token":"content.token"
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
                            "content.success",
                            true
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
        "step":{
            "name":"get token with $user_agent, $os_platform, $app_version",
            "request":{
                "url":"/api/get-token",
                "method":"POST",
                "headers":{
                    "app_version":"$app_version",
                    "os_platform":"$os_platform",
                    "user_agent":"$user_agent"
                },
                "json":{
                    "sign":"${get_sign($user_agent, $device_sn, $os_platform, $app_version)}"
                },
                "extract":[
                    {
                        "token":"content.token"
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
                            "content.success",
                            true
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
]]
    
    
    
"""