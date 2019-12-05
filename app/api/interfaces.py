# coding:utf-8
from flask import jsonify, request, url_for, current_app
from .. import db
from ..models import Interface,Project,System
from . import api

@api.route('/interfaces/')
def get_interfaces():
    page = request.args.get('page', 1, type=int)

    if request.args:
        sys_id = request.args.get('system_id')

        pagination = db.session.query(Interface.id, Interface.if_name, Interface.if_desc, Interface.status,
                                      Interface.protocol, Interface.method,
                                      Interface.url, Interface.autotest, Interface.project_id, Interface.system_id,
                                      Project.pro_name,
                                      System.sys_name).filter(Interface.system_id==sys_id if System.project_id is not None else "", Interface.status == 1).join(Project,
                                                                                Interface.project_id == Project.id).join(
            System, Interface.system_id == System.id) \
            .paginate(page, per_page=current_app.config['FLASKY_PER_PAGE'], error_out=False)

    else:

        pagination = db.session.query(Interface.id, Interface.if_name, Interface.if_desc, Interface.status, Interface.protocol,Interface.method,
                                      Interface.url, Interface.autotest, Interface.project_id, Interface.system_id,Project.pro_name,
                                      System.sys_name).filter_by(status=1).join(Project,Interface.project_id == Project.id).join(System,Interface.system_id == System.id)\
            .paginate(page, per_page=current_app.config['FLASKY_PER_PAGE'],error_out=False)

    interfaces = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_interfaces', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_interfaces', page=page+1)
    return jsonify({
        'code': 1,
        'interfaces': [{'id':interface.id,'if_name':interface.if_name,'if_desc':interface.if_desc,'status':interface.status,'protocol':interface.protocol,'method':interface.method,
                        'url':interface.url,'autotest':interface.autotest,'project_id':interface.project_id,'system_id':interface.system_id,'pro_name':interface.pro_name,'sys_name':interface.sys_name} for interface in interfaces],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/interfaces/<int:id>')
def get_interface(id):
    interface = Interface.query.get_or_404(id)
    return jsonify({
        'code': 1,
        'interface': interface.to_json()
    })

@api.route('/interfaces/', methods=['POST'])
def new_interface():
    interface = Interface.from_json(request.json)
    interface.status = 1
    db.session.add(interface)
    db.session.commit()
    return jsonify({
        'code': 1,
        'interface': interface.to_json()
})

@api.route('/interfaces/<int:id>', methods=['PUT'])
def edit_interface(id):
    interface = Interface.query.get_or_404(id)
    interface.if_name = request.json.get('if_name', interface.if_name)
    interface.if_desc = request.json.get('if_desc', interface.if_desc)
    interface.system_id = request.json.get('system_id', interface.system_id)
    interface.project_id = request.json.get('project_id', interface.project_id)
    interface.protocol = request.json.get('protocol', interface.protocol)
    interface.method = request.json.get('method', interface.method)
    interface.url = request.json.get('url', interface.url)
    interface.autotest = request.json.get('autotest', interface.autotest)
    db.session.add(interface)
    db.session.commit()
    return jsonify({
        'code': 1,
        'interface': interface.to_json()
    })

@api.route('/interfaces/<int:id>', methods=['DELETE'])
def delete_interface(id):
    interface = Interface.query.get_or_404(id)
    interface.status = 0
    db.session.add(interface)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})