#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 15:39
# @Author  : z.g

import json
import os
import requests
import random
import simplejson
from requests_toolbelt import MultipartEncoder
from requests import exceptions
from core.bin import log

Logger = log.Log()

def post(header, address, request_parameter_type, timeout=8, data=None, files=None):
    """
    post请求
    :param header: 请求头
    :param address: 请求地址
    :param request_parameter_type: 请求参数格式（form_data,raw）
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 文件路径
    :return:
    """
    if 'form_data' in request_parameter_type:
        for i in files:
            value = files[i]
            if '/' in value:
                file_parm = i
                files[file_parm] = (os.path.basename(value), open(value, 'rb'))
        enc = MultipartEncoder(
            fields=files,
            boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
        )
        header['Content-Type'] = enc.content_type

        response = requests.post(url=address, data=enc, headers=header, timeout=timeout)
    else:
        response = requests.post(url=address, data=data, headers=header, timeout=timeout, files=files)
    try:
        if response.status_code != 200:
            return response.status_code, response.text, response.headers, response.elapsed.total_seconds(), response.request.body, response.request.headers, response.request.url
        else:
            return response.status_code, response.json(), response.headers, response.elapsed.total_seconds(), response.request.body, response.request.headers, response.request.url
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except simplejson.errors.JSONDecodeError:
        return response.status_code, ''
    except exceptions.Timeout as e:
        Logger.exception(e)
        Logger.error(e)
        pass
    except Exception as e:
        Logger.exception('ERROR')
        Logger.error(e)
        pass


def get(header, address, data, timeout=8):
    """
    get请求
    :param header: 请求头
    :param address: 请求地址
    :param data: 请求参数
    :param timeout: 超时时间
    :return:
    """
    response = requests.get(url=address, params=data, headers=header, timeout=timeout)
    if response.status_code == 301:
        response = requests.get(url=response.headers["location"])
    try:
        return response.status_code, response.json(), response.headers, response.elapsed.total_seconds(), response.request.body, response.request.headers, response.request.url
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except simplejson.errors.JSONDecodeError:
        return response.status_code, ''
    except Exception as e:
        Logger.exception('ERROR')
        Logger.error(e)
        raise


def put(header, address, request_parameter_type, timeout=8, data=None, files=None):
    """
    post请求
    :param header: 请求头
    :param address: 请求地址
    :param request_parameter_type: 请求参数格式（form_data,raw）
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 文件路径
    :return:
    """
    if request_parameter_type == 'raw':
        data = json.dumps(data)
    response = requests.put(url=address, data=data, headers=header, timeout=timeout, files=files)
    try:
        return response.status_code, response.json(), response.headers, response.elapsed.total_seconds(), response.request.body, response.request.headers, response.request.url
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except simplejson.errors.JSONDecodeError:
        return response.status_code, ''
    except Exception as e:
        Logger.exception('ERROR')
        Logger.error(e)
        raise


def delete(header, address, data, timeout=8):
    """
    get请求
    :param header: 请求头
    :param address: 请求地址
    :param data: 请求参数
    :param timeout: 超时时间
    :return:
    """
    response = requests.delete(url=address, params=data, headers=header, timeout=timeout)

    try:
        return response.status_code, response.json(), response.headers, response.elapsed.total_seconds(), response.request.body, response.request.headers, response.request.url
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except simplejson.errors.JSONDecodeError:
        return response.status_code, ''
    except Exception as e:
        Logger.exception('ERROR')
        Logger.error(e)
        raise


def save_cookie(header, address, timeout=8, data=None, files=None):
    """
    保存cookie信息
    :param header: 请求头
    :param address: 请求地址
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 文件路径
    :return:
    """
    # PATH = os.getcwd()
    cookie_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs')) + '/cookie.txt'
    response = requests.post(url=address, data=data, headers=header, timeout=timeout, files=files)
    try:
        cookie = response.cookies.get_dict()
        for i in cookie:
            values = cookie[i]
            with open(cookie_path, 'w+', encoding='utf-8')as f:
                f.write(i+"="+values)
            Logger.debug("cookies已保存，结果为：%s" % (i+"="+values))
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except simplejson.errors.JSONDecodeError:
        return response.status_code, ''
    except Exception as e:
        Logger.exception('ERROR')
        Logger.error(e)
        raise