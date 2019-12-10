# coding:utf-8
from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Project
from . import api

@api.route('/projects/')
def get_projects():
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.filter_by(status=1).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'],
        error_out=False)
    projects = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_projects', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_projects', page=page+1)
    return jsonify({
        'code': 1,
        'projects': [project.to_json() for project in projects],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/projects/<int:id>')
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify({
        'code': 1,
        'data': project.to_json()
    })

@api.route('/projects/', methods=['POST'])
def new_project():
    project = Project.from_json(request.json)
    project.status = 1
    exist_project = Project.query.filter_by(pro_name=project.pro_name).first()
    if exist_project:
        return jsonify({'code':0, 'message': '该项目名称已存在'})
    db.session.add(project)
    db.session.commit()
    return jsonify({
        'code': 1,
        'projects': project.to_json()
    })

@api.route('/projects/<int:id>', methods=['PUT'])
def edit_project(id):
    project = Project.query.get_or_404(id)
    project.pro_name = request.json.get('pro_name', project.pro_name)
    project.pro_desc = request.json.get('pro_desc', project.pro_desc)
    db.session.add(project)
    db.session.commit()
    return jsonify({
        'code': 1,
        'project': project.to_json()
    })

@api.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    project.status = 0
    db.session.add(project)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})