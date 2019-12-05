#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 16:51
# @Author  : z.g

from core.bin import log

Logger = log.Log()

def extract(case, content, headers):
    extract_dict = {}
    if isinstance(content, str):
        content = eval(content)

    if case.get("case_extract") != None:
        Logger.info("响应提取字段: %s " % case.get("case_extract"))
        for key in case.get("case_extract"):
            if case.get("case_extract").get(key).split(".")[0] == "headers":
                extract_dict[key]=(extract_data(case.get("case_extract").get(key), headers))
                Logger.info("响应头提取字段: %s %s" % (key, extract_dict[key]))
            elif case.get("case_extract").get(key).split(".")[0] == "content":
                extract_dict[key]=(extract_data(case.get("case_extract").get(key), content))
                Logger.info("响应体提取字段: %s %s" % (key, extract_dict[key]))
        return extract_dict

    else:
        return {}

def extract_data(key, data):
    temp = {}
    locator = key.split(".")
    for i in range(1, len(locator)):
        if i == 1:
            temp[key] = data.get(locator[i])
            if temp[key] == None:
                Logger.error("从 %s 中提取字段 %s 失败" % (data, key))
                return temp
        else:
            try:
                temp[key] = temp[key].get(locator[i])
            except Exception as e:
                Logger.error("从 %s 中提取字段 %s 失败" % (temp[key], key))
                Logger.error(e)
                # pass
    return temp[key]
