#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 17:28
# @Author  : z.g

import os
import subprocess
import pytest

PATH = os.path.split(os.path.realpath(__file__))[0]
xml_report_path = PATH + "/report/xml"
html_report_path = PATH + "/report/html"

def invoke(cmd):
    output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    o = output.decode("utf-8")
    return o


if __name__ == '__main__':
    args = ['-s', '-q', '--alluredir', xml_report_path]
    pytest.main(args)
    cmd = 'allure generate %s -o %s' % (xml_report_path, html_report_path)
    invoke(cmd)
