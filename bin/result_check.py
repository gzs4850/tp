#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 9:47
# @Author  : z.g
import allure
from bin import log

Logger = log.Log()

def check_data(key, exp_dict, data):
    temp = {}
    locator = key.split(".")
    for i in range(1, len(locator)):
        if i == 1:
            temp[key] = data.get(locator[i])
            if temp[key] == None:
                Logger.error("从 %s 中提取字段 %s 失败" % (data, key))
                break
            # print("temp[key]:%s" % temp[key])
        else:
            try:
                temp[key] = temp[key].get(locator[i])
            except Exception as e:
                Logger.error(e)
                Logger.error("无法找到需校验的字段 %s" %key)

    if str(temp[key]) == str(exp_dict[key]):
        with allure.step("校验返回数据"):
            allure.attach("期望结果", str(exp_dict[key]))
            allure.attach("实际结果", str(temp[key]))
        # print("pass %s %s" % (key, temp[key]))
        Logger.info("断言成功：%s 期望结果 %s, 实际结果 %s" % (key, str(temp[key]), str(exp_dict[key])))
        return True
    else:
        # print("fail %s, expect value is %s, real value is %s" % (key, exp_dict[key], temp[key]))
        Logger.error("断言失败：%s 期望结果 %s, 实际结果 %s" % (key, exp_dict[key], temp[key]))
        return False

def check(case, code, content, headers):
    # print("content:%s" %content)
    # print("headers:%s" % headers)
    exp_dict = case.get("case_validate")
    if isinstance(content, str):
        content = eval(content)

    if exp_dict != None:
        for key in exp_dict.keys():
            with allure.step("校验HTTP响应状态"):
                allure.attach("期望结果", str(exp_dict["status_code"]))
                allure.attach("实际结果", str(code))
            if key == "status_code":
                if exp_dict["status_code"] == code:
                    Logger.info("断言成功：%s 期望结果 %s, 实际结果 %s" % (key, exp_dict["status_code"], code))
                    # print("pass %s:%s" %(key, code))
                    pass
                else:
                    Logger.error("断言失败：%s 期望结果 %s, 实际结果 %s" % (key, exp_dict["status_code"], code))
                    # print("fail, expect value is %s, real value is %s" %(exp_dict["status_code"], code))
                    return False

            elif key.split(".")[0] == "headers":
                return check_data(key, exp_dict, headers)
            elif key.split(".")[0] == "content":
                return check_data(key, exp_dict, content)

    else:
        allure.step("不需要校验结果")
        Logger.info("不需要校验结果")
    return True

