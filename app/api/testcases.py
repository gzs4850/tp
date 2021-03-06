# coding:utf-8
import json

from flask import jsonify, request, g, url_for, current_app
from sqlalchemy import and_

# import app
from .. import db, scheduler
from ..models import Testcase, Caserefer, Interface, System, Project, Caseextract, Assertrule, Baseurl
from . import api
from core.bin.api_exec import exec_api


@api.route('/testcases')
def get_testcases():
    page = request.args.get('page', 1, type=int)

    pagination = db.session.query(Testcase.id, Testcase.case_name, Testcase.method, Testcase.url, Testcase.request_head,
                                  Testcase.request_json, Testcase.check_json, Testcase.extract_json, Testcase.var_json,
                                  Testcase.status,
                                  Interface.if_name, System.sys_name, Project.pro_name, Testcase.interface_id,
                                  Interface.system_id, Interface.project_id, Interface.method,
                                  Interface.protocol).filter_by(status=1).join(
        Interface, Testcase.interface_id == Interface.id).join(Project, Interface.project_id == Project.id).join(System,
                                                                                                                 Interface.system_id == System.id) \
        .paginate(page, per_page=current_app.config['FLASKY_PER_PAGE'], error_out=False)

    # pagination = Testcase.query.filter_by(status=1).paginate(
    #     page, per_page=current_app.config['FLASKY_PER_PAGE'],
    #     error_out=False)

    testcases = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_projects', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_projects', page=page + 1)
    return jsonify({
        'code': 1,
        'testcases': [
            {'id': testcase.id, 'case_name': testcase.case_name, 'method': testcase.method, 'url': testcase.url,
             'request_head': testcase.request_head, 'request_json': testcase.request_json,
             'check_json': testcase.check_json, 'var_json': testcase.var_json,
             'extract_json': testcase.extract_json, 'status': testcase.status, 'if_name': testcase.if_name,
             'sys_name': testcase.sys_name, 'pro_name': testcase.pro_name,
             'interface_id': testcase.interface_id, 'system_id': testcase.system_id,
             'project_id': testcase.project_id, 'protocol': testcase.protocol} for
            testcase in testcases],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/testcaselist')
def get_testcaselist():
    page = request.args.get('page', 1, type=int)
    id = request.args.get("id")
    name = request.args.get("ifcase_name")
    system_id = request.args.get("system_id")
    project_id = request.args.get("project_id")

    condition = (Testcase.status == 1)
    if id:
        condition = and_(condition, Testcase.id == id)
    if name:
        condition = and_(condition, Testcase.case_name.like('%{0}%'.format(name)))
    if system_id:
        condition = and_(condition, Interface.system_id == system_id)
    if project_id:
        condition = and_(condition, Interface.project_id == project_id)

    pagination = db.session.query(Testcase.id, Testcase.case_name, Testcase.url, Testcase.method, Testcase.request_head,
                                  Testcase.request_json, Testcase.check_json, Testcase.extract_json, Testcase.var_json,
                                  Testcase.status,
                                  Interface.if_name, System.sys_name, Project.pro_name, Testcase.interface_id,
                                  Interface.system_id, Interface.project_id,
                                  Interface.protocol).filter(condition).join(Interface,
                                                                             Testcase.interface_id == Interface.id).join(
        Project, Interface.project_id == Project.id).join(System, Interface.system_id == System.id).paginate(page,
                                                                                                             per_page=
                                                                                                             current_app.config[
                                                                                                                 'FLASKY_PER_PAGE'],
                                                                                                             error_out=False)

    testcases = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_projects', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_projects', page=page + 1)
    return jsonify({
        'code': 1,
        'testcases': [{'id': testcase.id, 'case_name': testcase.case_name, 'url': testcase.url,
                       'request_head': testcase.request_head, 'request_json': testcase.request_json,
                       'check_json': testcase.check_json, 'var_json': testcase.var_json,
                       'extract_json': testcase.extract_json, 'status': testcase.status, 'if_name': testcase.if_name,
                       'sys_name': testcase.sys_name, 'pro_name': testcase.pro_name,
                       'interface_id': testcase.interface_id, 'system_id': testcase.system_id,
                       'project_id': testcase.project_id, 'method': testcase.method, 'protocol': testcase.protocol} for
                      testcase in testcases],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/testcases/<int:id>')
def get_testcase(id):
    testcases = Testcase.query.filter_by(id=id)
    return jsonify({
        'code': 1,
        'testcases': [testcase.to_json() for testcase in testcases]
    })


@api.route('/testcases', methods=['POST'])
def new_testcase():
    testcase = Testcase.from_json(request.json)
    db.session.add(testcase)
    db.session.commit()
    return jsonify({
        'code': 1,
        'testcase': testcase.to_json()
    })


@api.route('/testcases/<int:id>', methods=['PUT'])
def edit_testcase(id):
    testcase = Testcase.query.get_or_404(id)
    testcase.case_name = request.json.get('case_name', testcase.case_name)
    testcase.method = request.json.get('method', testcase.method)
    testcase.interface_id = request.json.get('interface_id', testcase.interface_id)
    testcase.request_json = json.dumps(request.json.get('request_json', testcase.request_json))
    testcase.request_head = json.dumps(request.json.get('request_head', testcase.request_head))
    testcase.url = request.json.get('if_url', testcase.url)
    testcase.response_json = json.dumps(request.json.get('response_json', None))
    testcase.response_head = json.dumps(request.json.get('response_head', None))
    testcase.check_json = json.dumps(request.json.get('check_json', testcase.check_json))
    testcase.extract_json = json.dumps(request.json.get('extract_json', testcase.extract_json))
    testcase.var_json = json.dumps(request.json.get('var_json', testcase.var_json))
    db.session.add(testcase)
    db.session.commit()
    return jsonify({
        'code': 1,
        'testcase': testcase.to_json()
    })


@api.route('/testcases/<int:id>', methods=['DELETE'])
def delete_testcase(id):
    testcase = Testcase.query.get_or_404(id)
    testcase.status = 0
    db.session.add(testcase)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})


# 单独执行一个case
@api.route('/testcases/run/<int:id>', methods=['POST'])
def run_single_testcase(id):
    pch = ''
    env = request.args.get("env")
    run(id, env, pch)
    return jsonify({
        'code': 1,
        'message': '执行成功'
    })


# 根据项目、系统分类执行case
@api.route('/testcases/run', methods=['POST'])
def run_testcase_by_condition(env, project_id, system_id):
    # system_id = request.args.get("system_id")
    # project_id = request.args.get("project_id")
    import time
    pch = str(round(time.time()*1000))

    with scheduler.app.app_context():

        condition = (Testcase.is_case == 1)
        if system_id:
            condition = and_(condition, Interface.system_id == system_id)
        if project_id:
            condition = and_(condition, Interface.project_id == project_id)

        ids = db.session.query(Testcase.id).filter(condition).join(Interface, Testcase.interface_id == Interface.id).join(
            Project, Interface.project_id == Project.id).join(System, Interface.system_id == System.id)

        for id in ids:
            print(id[0])
            run(id[0], env, pch)

        return jsonify({
            'code': 1,
            'message': '执行成功'
        })


# 用例执行
def run(id, env, pch):
    caserefers = Caserefer.query.filter_by(mockid=id).order_by(Caserefer.ordernum).all()
    # print("referCase: %s" %caserefers)
    testsuit = []
    cases = []
    if len(caserefers) > 0:
        for caserefer in caserefers:
            print("mockid: %s" % caserefer.refer_mockid)
            dict_case = {}

            dict_case["case"] = package_case(caserefer.refer_mockid, env)
            cases.append(dict_case)

    dict_case = {}
    dict_case["case"] = package_case(id, env)
    cases.append(dict_case)

    print("cases: %s" % cases)
    testsuit.append(cases)
    testsuit = json.dumps(testsuit)
    print("testsuit: %s" % testsuit)
    exec_api(testsuit=str(testsuit), pch=pch)


# 封装case
def package_case(case_id, env):
    case = {}
    case['request'] = {}
    testcase = Testcase.query.get_or_404(case_id)
    case['name'] = testcase.to_json().get('case_name')
    case['id'] = testcase.to_json().get('id')
    case['baseurl'] = getBaseurl(testcase.to_json().get('interface_id'), env)
    case['request']['variable'] = testcase.to_json().get('var_json')
    case['request']['url'] = testcase.to_json().get('url')
    case['request']['method'] = testcase.to_json().get('method')
    case['request']['headers'] = testcase.to_json().get('request_head')
    case['request']['json'] = testcase.to_json().get('request_json')
    case['request']['extract'] = testcase.to_json().get('extract_json')
    case['request']['validate'] = testcase.to_json().get('check_json')
    case['request']['setup_hooks'] = []
    case['request']['teardown_hooks'] = []
    return case


# 获取环境URL
def getBaseurl(interface_id, env):
    print("---------interface_id-----------:%s" % interface_id)
    baseurl = db.session.query(Baseurl).join(System, System.id == Baseurl.system_id).join(Interface,
                                                                                          System.id == Interface.system_id).join(
        Testcase, Interface.id == Testcase.interface_id).filter(Testcase.interface_id == interface_id).first()
    print("---------baseurl-----------:%s" % baseurl.qa_url)
    if env == "uat":
        return baseurl.qa_url
    else:
        return baseurl.pro_url


@api.route('/runtestcase/<int:id>', methods=['POST'])
def run_testcase(id):
    testset = load_testcases(id)
    print('testset:%s', testset)
    # single_run(testset)
    return jsonify({'code': 1, 'message': '执行成功'})


def load_testcases(caseid):
    testsets = []
    testcases = []
    caselist = get_referCase(caseid)
    print('testcaseList:%s', caselist)
    for caseid in caselist:
        testcase = Testcase.query.get_or_404(caseid)
        case_name = testcase.to_json().get('case_name')
        interface_id = testcase.to_json().get('interface_id')
        request_json = testcase.to_json().get('request_json')
        request_head = testcase.to_json().get('request_head')
        url = testcase.to_json().get('url')
        check_json = testcase.to_json().get('check_json')
        ref_json = testcase.to_json().get('ref_json')
        is_case = testcase.to_json().get('is_case')
        interface = Interface.query.filter_by(id=interface_id).first()
        print(interface)
        method = interface.to_json().get('method')
        testcases.append({'case_name': case_name,
                          'request': {'url': url, 'headers': request_head, 'method': method,
                                      'json': request_json}, 'variables': [], 'extract': ref_json,
                          'validate': check_json})
    dict = {'name': '', 'config': '', 'api': '', 'testcases': testcases}
    testsets.append(dict)
    return testsets


@api.route('/testcases/refercase/<int:id>')
def get_referCase(id):
    # referlist = []
    # caserefers = Caserefer.query.filter_by(mockid=id).order_by(Caserefer.ordernum).all()
    # if caserefer:
    #     for case in caserefer:
    #         referlist.append(case.to_json().get('refer_mockid'))
    #     referlist.append(id)
    #     return referlist

    caserefers = db.session.query(Caserefer.id, Caserefer.mockid, Caserefer.refer_mockid, Caserefer.ordernum,
                                  Testcase.case_name).filter_by(mockid=id).order_by(db.asc(Caserefer.ordernum)).join(
        Testcase, Caserefer.refer_mockid == Testcase.id)

    return jsonify({
        'code': 1,
        'caserefers': [{'id': caserefer.id, 'mockid': caserefer.mockid, 'refer_mockid': caserefer.refer_mockid,
                        'ordernum': caserefer.ordernum, 'refer_casename': caserefer.case_name} for
                       caserefer in caserefers]
    })


@api.route('/testcases/refercase/<int:id>', methods=['PUT'])
def new_referCase(id):
    ordernum = 1
    # print('----request.json----------%s' % request.json)
    for req in request.json:
        reqlist = {}
        # print('-----req---------%s' %req)
        caserefer = Caserefer.query.filter_by(mockid=id).order_by(
            db.desc(Caserefer.ordernum)).first()
        if caserefer:
            ordernum = int(caserefer.ordernum) + 1
            # print(ordernum)
        reqlist['ordernum'] = ordernum
        reqlist['mockid'] = id
        reqlist['refer_mockid'] = req['id']
        caserefer = Caserefer.from_json(reqlist)
        db.session.add(caserefer)
        db.session.commit()
    return jsonify({
        'code': 1,
        'caserefer': caserefer.to_json()
    })


@api.route('/testcases/refercase/<int:id>', methods=['DELETE'])
def delete_referCase(id):
    caserefer = Caserefer.query.get_or_404(id)
    db.session.delete(caserefer)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})


@api.route('/testcases/caseextract/<int:id>')
def get_caseExtract(id):
    caseextracts = db.session.query(Caseextract.id, Caseextract.mockid, Caseextract.extract_name,
                                    Caseextract.extract_value, Testcase.case_name).filter_by(mockid=id).join(
        Testcase, Caseextract.mockid == Testcase.id)

    return jsonify({
        'code': 1,
        'caseextracts': [{'id': caseextract.id, 'mockid': caseextract.mockid, 'extract_name': caseextract.extract_name,
                          'extract_value': caseextract.extract_value, 'refer_casename': caseextract.case_name} for
                         caseextract in caseextracts]
    })


@api.route('/testcases/caseextract/', methods=['POST'])
def new_caseExtract():
    caseextract = Caseextract.from_json(request.json)
    db.session.add(caseextract)
    db.session.commit()
    return jsonify({
        'code': 1,
        'caseextract': caseextract.to_json()
    })


@api.route('/testcases/caseextract/<int:id>', methods=['DELETE'])
def delete_caseExtract(id):
    caseextract = Caseextract.query.get_or_404(id)
    db.session.delete(caseextract)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})


@api.route('/testcases/assertrule/<int:id>')
def get_assertRule(id):
    assertrules = db.session.query(Assertrule.id, Assertrule.mockid, Assertrule.assert_type, Assertrule.exp_value,
                                   Assertrule.act_value, Testcase.case_name).filter_by(mockid=id).join(
        Testcase, Assertrule.mockid == Testcase.id)

    return jsonify({
        'code': 1,
        'assertrules': [{'id': assertrule.id, 'mockid': assertrule.mockid, 'assert_type': assertrule.assert_type,
                         'exp_value': assertrule.exp_value, 'act_value': assertrule.act_value,
                         'refer_casename': assertrule.case_name} for
                        assertrule in assertrules]
    })


@api.route('/testcases/assertrule/', methods=['POST'])
def new_assertRule():
    assertrule = Assertrule.from_json(request.json)
    db.session.add(assertrule)
    db.session.commit()
    return jsonify({
        'code': 1,
        'assertrule': assertrule.to_json()
    })


@api.route('/testcases/assertrule/<int:id>', methods=['DELETE'])
def delete_assertRule(id):
    assertrule = Assertrule.query.get_or_404(id)
    db.session.delete(assertrule)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})
