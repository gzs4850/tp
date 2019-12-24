#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/23 11:39
# @Author  : z.g
from flask import request, jsonify
from sqlalchemy import and_
from app import db
from app.api import api
from app.models import Baseurl, System, Project


@api.route('/baseurls')
def get_baseurl():
    id = request.args.get("id")
    url_name = request.args.get("url_name")
    system_id = request.args.get("system_id")
    condition = (1 == 1)
    if id:
        condition = and_(condition, Baseurl.id == id)
    if url_name:
        condition = and_(condition, Baseurl.url_name.like('%{0}%'.format(url_name)))
    if system_id:
        condition = and_(condition, Baseurl.system_id == system_id)

    baseurls = db.session.query(Baseurl.id, Baseurl.url_name, Baseurl.qa_url, Baseurl.pro_url, Baseurl.system_id,
                                System.sys_name, Baseurl.project_id, Project.pro_name).filter(condition).join(System,
                                                                                                              Baseurl.system_id == System.id).join(Project,
                                                                                                              Baseurl.project_id == Project.id)
    return jsonify({
        'code': 1,
        'baseurls': [
            {'id': baseurl.id, 'url_name': baseurl.url_name, 'qa_url': baseurl.qa_url, 'pro_url': baseurl.pro_url,
             'system_id': baseurl.system_id, 'sys_name': baseurl.sys_name, 'project_id': baseurl.project_id, 'pro_name': baseurl.pro_name} for baseurl
            in baseurls],
    })

@api.route('/baseurls', methods = ["POST"])
def new_baseurl():
    baseurl = Baseurl.from_json(request.json)
    exist_baseurl = Baseurl.query.filter_by(url_name=baseurl.url_name, system_id=baseurl.system_id).first()
    if exist_baseurl:
        return jsonify({'code': 0, 'message': '该系统URL已存在'})
    db.session.add(baseurl)
    db.session.commit()
    return jsonify({
        'code': 1,
        'baseurl': baseurl.to_json()
    })

@api.route('/baseurls/<int:id>', methods=['PUT'])
def edit_baseurl(id):
    baseurl = Baseurl.query.get_or_404(id)
    baseurl.url_name = request.json.get('url_name', baseurl.url_name)
    baseurl.qa_url = request.json.get('qa_url', baseurl.qa_url)
    baseurl.pro_url = request.json.get('pro_url', baseurl.pro_url)
    baseurl.system_id = request.json.get('system_id', baseurl.system_id)
    baseurl.project_id = request.json.get('project_id', baseurl.project_id)
    db.session.add(baseurl)
    db.session.commit()
    return jsonify({
        'code': 1,
        'baseurl': baseurl.to_json()
    })

@api.route('/baseurls/<int:id>', methods=['DELETE'])
def delete_baseurl(id):
    baseurl = Baseurl.query.get_or_404(id)
    db.session.delete(baseurl)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})
