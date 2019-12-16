# coding:utf-8
from flask import jsonify, request, g, url_for, current_app
from sqlalchemy import and_

from .. import db
from ..models import System,Project
from . import api

@api.route('/systems')
def get_systems():
    page = request.args.get('page', 1, type=int)

    if request.args:
        pro_id = request.args.get('project_id')
        pagination = db.session.query(System.id, System.sys_name, System.sys_desc, System.status, System.project_id,Project.pro_name)\
            .filter(System.project_id==pro_id if System.project_id is not None else "", System.status == 1)\
            .join(Project,System.project_id == Project.id).paginate(page, per_page=current_app.config['FLASKY_PER_PAGE'],error_out=False)

    else:
        pagination = db.session.query(System.id, System.sys_name, System.sys_desc, System.status, System.project_id, Project.pro_name).filter_by(status = 1).join(Project,System.project_id == Project.id).paginate(
            page, per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)

    systems = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_systems', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_systems', page=page+1)
    return jsonify({
        'code': 1,
        # 'systems': [system.to_json() for system in systems],
        'systems': [{'id':system.id,'sys_name':system.sys_name,'sys_desc':system.sys_desc,'status':system.status,'project_id':system.project_id,'pro_name':system.pro_name} for system in systems],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/systems/<int:id>')
def get_system(id):
    system = System.query.get_or_404(id)
    return jsonify({
        'code': 1,
        'system': system.to_json()
    })

@api.route('/systemsbysearch')
def search_system():
    page = request.args.get('page', 1, type=int)
    id = request.args.get("id")
    name = request.args.get("sys_name")
    project_id = request.args.get("project_id")
    condition = (System.status == 1)
    if id:
        condition = and_(condition, System.id == id)
    if name:
        condition = and_(condition, System.sys_name.like('%{0}%'.format(name)))
    if project_id:
        condition = and_(condition, System.project_id == project_id)

    pagination = db.session.query(System.id, System.sys_name, System.sys_desc, System.status, System.project_id, Project.pro_name).filter(condition).\
        join(Project,System.project_id == Project.id).paginate(page, per_page=current_app.config['FLASKY_PER_PAGE'],error_out=False)
    systems = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_systems', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_systems', page=page + 1)
    return jsonify({
        'code': 1,
        # 'systems': [system.to_json() for system in systems],
        'systems': [{'id': system.id, 'sys_name': system.sys_name, 'sys_desc': system.sys_desc, 'status': system.status,
                     'project_id': system.project_id, 'pro_name': system.pro_name} for system in systems],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/systems', methods=['POST'])
def new_system():
    system = System.from_json(request.json)
    system.status = 1
    exist_system = System.query.filter_by(sys_name=system.sys_name,project_id=system.project_id).first()
    if exist_system:
        return jsonify({'code':0, 'message': '该系统名称已存在'})
    db.session.add(system)
    db.session.commit()
    return jsonify({
        'code': 1,
        'system': system.to_json()
    })

@api.route('/systems/<int:id>', methods=['PUT'])
def edit_system(id):
    system = System.query.get_or_404(id)
    system.sys_name = request.json.get('sys_name', system.sys_name)
    system.sys_desc = request.json.get('sys_desc', system.sys_desc)
    system.project_id = request.json.get('project_id', system.project_id)
    db.session.add(system)
    db.session.commit()
    return jsonify({
        'code': 1,
        'system': system.to_json()
    })

@api.route('/systems/<int:id>', methods=['DELETE'])
def delete_system(id):
    system = System.query.get_or_404(id)
    system.status = 0
    db.session.add(system)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})