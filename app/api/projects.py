# coding:utf-8
from flask import jsonify, request, g, url_for, current_app
from sqlalchemy.sql.elements import and_

from .. import db
from ..models import Project
from . import api

@api.route('/projects')
def get_projects():
    page = request.args.get('currentPage', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    id = request.args.get('id')
    pro_name = request.args.get('pro_name')

    condition = (Project.status==1)
    if id:
        condition = and_(Project.id==id)
    if pro_name:
        condition = and_(Project.pro_name.like('%{0}%'.format(pro_name)))

    pagination = Project.query.filter(condition).paginate(page, per_page,error_out=False)
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

# @api.route('/projects/<int:id>')
# def get_project(id):
#     project = Project.query.get_or_404(id)
#     return jsonify({
#         'code': 1,
#         'projects': project.to_json()
#     })

@api.route('/projects/<int:id>')
def get_project(id):
    projects = Project.query.filter_by(id = id)
    return jsonify({
        'code': 1,
        'projects': [project.to_json() for project in projects]
    })

@api.route('/projectsbyname/<string:name>')
def get_project_byname(name):
    projects = Project.query.filter(Project.pro_name.like('%{0}%'.format(name))).all()
    return jsonify({
        'code': 1,
        'projects': [project.to_json() for project in projects]
    })

@api.route('/projects', methods=['POST'])
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
    print("json: %s" % request.json)
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