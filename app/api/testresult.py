# coding:utf-8
import json
import time
from datetime import datetime
from decimal import Decimal

from flask import jsonify, request, url_for, current_app
from ..models import Testresult, Testcase, Interface, System, Project
from . import api
from .. import db
from sqlalchemy import and_, func


@api.route('/testresults/<int:id>')
def get_testresult(id):
    testresult = db.session.query(Testresult).filter(Testresult.case_id == id).order_by(Testresult.id.desc()).first()

    if testresult:
        return jsonify({
            'code': 1,
            'testresult': testresult.to_json()
        })
    else:
        return jsonify({
            'code': 1,
            'testresult': {}
        })


@api.route('/testresults')
def get_testresults():
    page = request.args.get('page', 1, type=int)
    id = request.args.get("id")
    name = request.args.get("case_name")
    interface_id = request.args.get("interface_id")
    system_id = request.args.get("system_id")
    project_id = request.args.get("project_id")

    condition = (1 == 1)
    if id:
        condition = and_(Testresult.case_id == id)
    if name:
        condition = and_(condition, Testcase.case_name.like('%{0}%'.format(name)))
    if interface_id:
        condition = and_(condition, Testcase.interface_id == interface_id)
    if system_id:
        condition = and_(condition, Interface.system_id == system_id)
    if project_id:
        condition = and_(condition, Interface.project_id == project_id)

    pagination = db.session.query(Testresult.id, Testresult.case_id, Testcase.case_name, Testresult.test_result,
                                  Testresult.real_rsp_code, Testresult.real_req_path,
                                  Testresult.real_req_head, Testresult.real_req_json, Testresult.real_rsp_head,
                                  Testresult.real_rsp_json, Testresult.real_rsp_time,
                                  Testresult.timestamp, Testresult.assert_msg, Testresult.batch_number,
                                  Interface.if_name, System.sys_name, Project.pro_name,
                                  Testcase.interface_id, Interface.system_id, Interface.project_id).filter(
        condition).join(Testcase, Testresult.case_id == Testcase.id).join(Interface,
                                                                          Testcase.interface_id == Interface.id).join(
        Project, Interface.project_id == Project.id).join(System, Interface.system_id == System.id).paginate(page,
                                                                                                             per_page=
                                                                                                             current_app.config[
                                                                                                                 'FLASKY_PER_PAGE'],
                                                                                                             error_out=False)

    testresults = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_testresults', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_testresults', page=page + 1)
    return jsonify({
        'code': 1,
        'testresults': [{'id': testresult.id, 'case_id': testresult.case_id, 'case_name': testresult.case_name,
                         'test_result': testresult.test_result,
                         'real_rsp_code': testresult.real_rsp_code, 'real_req_path': testresult.real_req_path,
                         'real_req_head': testresult.real_req_head, 'real_req_json': testresult.real_req_json,
                         'real_rsp_head': testresult.real_rsp_head, 'real_rsp_json': testresult.real_rsp_json,
                         'real_rsp_time': testresult.real_rsp_time,
                         'timestamp': datetime.strftime(testresult.timestamp, "%Y-%m-%d %H:%M:%S"),
                         'assert_msg': testresult.assert_msg, 'batch_number': testresult.batch_number,
                         'if_name': testresult.if_name, 'sys_name': testresult.sys_name,
                         'pro_name': testresult.pro_name,
                         'interface_id': testresult.interface_id, 'system_id': testresult.system_id,
                         'project_id': testresult.project_id} for
                        testresult in testresults],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/resultstatistic')
def get_success_rate():
    response = {}
    try:
        ret_list = db.session.query(Testresult.batch_number,
                                        func.count(Testresult.id),
                                        func.count(func.if_(Testresult.test_result == 'pass', True, None)),
                                        func.count(func.if_(Testresult.test_result == 'fail', True, None)),
                                        func.count(func.if_(Testresult.test_result == 'pass', True, None)) / func.count(
                                            Testresult.id)).group_by(
            Testresult.batch_number).order_by(db.desc(Testresult.batch_number)).limit(15).all()
        print(ret_list)
        info_list = []
        for ret in ret_list:
            info = {
                'time':time.strftime("%H:%M:%S", time.localtime(int(ret[0][0:10]))),
                'total':ret[1],
                'pass':ret[2],
                'fail':ret[3],
                'rate':float(str(Decimal(ret[4]).quantize(Decimal('0.00'))))
            }
            info_list.append(info)
        # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ret[0]))),
        response['testresult'] = info_list
        response['count'] = len(info_list)
        response['msg'] = "Get case result success!"
        response['code'] = 1
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)
    # for a in success_rate:
    #     print(a)
    #     return jsonify({
    #         'code': 1,
    #         'success_rate': success_rate
    #     })
