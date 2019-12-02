#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 9:47
# @Author  : z.g
import allure
import json

def is_json(result):
    try:
        json.load(result)
    except ValueError:
        return False
    return True

def check_data(key, exp_dict, data):
    temp = {}
    locator = key.split(".")
    # print("locator:%s" % locator)
    # print(locator[0])
    # if len(locator) == 2:
    #     if str(data.get(locator[1])) == str(exp_dict[key]):
    #         with allure.step("校验返回数据"):
    #             allure.attach("期望结果", str(exp_dict[key]))
    #             allure.attach("实际结果", str(data.get(locator[1])))
    #         print("pass %s %s" % (key, data.get(locator[1])))
    #     else:
    #         print(
    #             "check fail, expect value is %s, real value is %s" % (exp_dict[key], data.get(locator[1])))
    #         return False
    # else:
    #     print(len(locator))
    for i in range(1, len(locator)):
        if i == 1:
            temp[key] = data.get(locator[i])
            # print("temp[key]:%s" % temp[key])
        else:
            temp[key] = temp[key].get(locator[i])
    if str(temp[key]) == str(exp_dict[key]):
        with allure.step("校验返回数据"):
            allure.attach("期望结果", str(exp_dict[key]))
            allure.attach("实际结果", str(temp[key]))
        print("pass %s %s" % (key, temp[key]))
        return True
    else:
        print("fail %s, expect value is %s, real value is %s" % (key, exp_dict[key], temp[key]))
        return False

def check(case, code, content, headers):
    # print("content:%s" %content)
    # print("headers:%s" % headers)
    exp_dict = case.get("case_validate")
    # print(exp_dict)
    if exp_dict != None:

        # print(exp_dict.keys())
        for key in exp_dict.keys():
            with allure.step("校验HTTP响应状态"):
                allure.attach("期望结果", str(exp_dict["status_code"]))
                allure.attach("实际结果", str(code))
            if key == "status_code":
                if exp_dict["status_code"] == code:
                    print("pass %s:%s" %(key, code))
                else:
                    print("fail, expect value is %s, real value is %s" %(exp_dict["status_code"], code))
                    return False

            elif key.split(".")[0] == "headers":
                check_data(key, exp_dict, headers)
            elif key.split(".")[0] == "content":
                check_data(key, exp_dict, content)

    else:
        allure.step("不需要校验结果")
    return True
