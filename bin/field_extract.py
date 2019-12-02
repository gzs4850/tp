#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 16:51
# @Author  : z.g

def extract(case, content, headers):
    extract_dict = {}

    if case.get("case_extract") != None:
        for key in case.get("case_extract"):
            if case.get("case_extract").get(key).split(".")[0] == "headers":
                extract_dict[key]=(extract_data(case.get("case_extract").get(key), headers))
            elif case.get("case_extract").get(key).split(".")[0] == "content":
                extract_dict[key]=(extract_data(case.get("case_extract").get(key), content))
        return extract_dict

    else:
        return {}

def extract_data(key, data):
    temp = {}
    locator = key.split(".")
    for i in range(1, len(locator)):
        if i == 1:
            temp[key] = data.get(locator[i])
        else:
            temp[key] = temp[key].get(locator[i])
    return temp[key]
