#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 17:42
# @Author  : z.g
from . import api
from flask import jsonify


@api.route('/user/login', methods=['POST'])
def login():
    return jsonify({
        'code': 1,
        'token': 'fdsjfhjkdshfkldsajfjasdfbjsdkfhsdajfj',
        'result': {
            'id': '100001',
            'name': '林锦泽',
            'roles': ['admin']
        }
    })


@api.route('/user/register', methods=['POST'])
def register():
    return jsonify({
        'code': 1
    })


@api.route('/user/info', methods=['POST'])
def userinfo():
    return jsonify({
        'code': 1,
        'id': '100001',
        'name': '林锦泽',
        'roles': ['admin'],
        'permissions': [
            {
                # // 一个页面一个对象，以name确定（对应静态路由表里面的name）
                'name': 'index'
            }, {
                'name': 'table'
            }, {
                'name': 'interface'
            },{
                'name': 'ifcase'
            }, {
                'name': 'project'
            }, {
                'name': 'system'
            }, {
                'name': 'userPassword'
            }, {
                'name': 'level4'
            }, {
                'name': 'level4Detail',
                # // permission存储数据级权限控制
                'permission': ['modify', 'delete']
            }
        ]
    })
