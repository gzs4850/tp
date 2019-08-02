#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 14:34
# @Author  : z.g
import re

# use $$ to escape $ notation
dolloar_regex_compile = re.compile(r"\$\$")
# variable notation, e.g. ${var} or $var
variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# function notation, e.g. ${func1($var_1, $var_3)}
function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")

def pre_testcase(testcase):
    pass


def field_extract(response):
    pass

def regex_findall_functions(content):
    """ extract all functions from string content, which are in format ${fun()}
    """
    try:
        return function_regex_compile.findall(content)
    except TypeError:
        return []


# print(regex_findall_functions("${func(a=1, b=2)}"))

testcase = '{"request": {"url": "/ajaxLogin/abc${func(a=${abc}, b=2)}/${efg}", "headers": {"Content-Type": "application/json"},"method": "POST", "json": {"username":"${fund()}${fune(f=0)}","password":"e10adc3949ba59abbe56e057f20f883e","isRememberPwd":false}}, "name": "7050用户登录", "content_type": "application/json", "validate": [{"comparator": "equals", "check": "code", "expected": "000"}]}'


# print(function_regex_compile.findall(testcase))

print(re.findall(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}", testcase))

print(re.findall(r"\$\{(\w+)\(()\)\}", testcase))

print(re.findall(r"\$\{.*?\(+.*?\)+.*?\}", testcase))