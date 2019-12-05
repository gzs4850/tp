from datetime import datetime
from . import db
from app.exceptions import ValidationError
import json


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pro_name = db.Column(db.String(64))
    pro_desc = db.Column(db.Text)
    status = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    systems = db.relationship('System', backref='project')
    interfaces = db.relationship('Interface', backref='project')

    def to_json(self):
        json_project = {
            'id': self.id,
            'pro_name': self.pro_name,
            'pro_desc': self.pro_desc,
            'status': self.status,
            'timestamp': self.timestamp
        }
        return json_project

    @staticmethod
    def from_json(json_project):
        pro_name = json_project.get('pro_name')
        pro_desc = json_project.get('pro_desc')
        if pro_name is None or pro_name == '':
            raise ValidationError('name is null')
        return Project(pro_name=pro_name, pro_desc=pro_desc)


class System(db.Model):
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_name = db.Column(db.String(64))
    sys_desc = db.Column(db.Text)
    status = db.Column(db.Boolean)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    interfaces = db.relationship('Interface', backref='system')

    def to_json(self):
        json_system = {
            'id': self.id,
            'sys_name': self.sys_name,
            'sys_desc': self.sys_desc,
            'status': self.status,
            'project_id': self.project_id,
            'timestamp': self.timestamp
        }
        return json_system

    @staticmethod
    def from_json(json_system):
        sys_name = json_system.get('sys_name')
        sys_desc = json_system.get('sys_desc')
        project_id = json_system.get('project_id')
        if sys_name is None or sys_name == '':
            raise ValidationError('sys_name is null')
        if project_id is None or project_id == '':
            raise ValidationError('project is null')
        return System(sys_name=sys_name, sys_desc=sys_desc, project_id=project_id)


class Interface(db.Model):
    __tablename__ = 'interfaces'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    if_name = db.Column(db.String(64))
    if_desc = db.Column(db.Text)
    method = db.Column(db.String(32))
    protocol = db.Column(db.String(32))
    url = db.Column(db.String(128))
    autotest = db.Column(db.String(2))
    status = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    testcases = db.relationship('Testcase', backref='interface')

    def to_json(self):
        json_interface = {
            'id': self.id,
            'if_name': self.if_name,
            'if_desc': self.if_desc,
            'method': self.method,
            'protocol': self.protocol,
            'url': self.url,
            'autotest': self.autotest,
            'status': self.status,
            'timestamp': self.timestamp,
            'system_id': self.system_id,
            'project_id': self.project_id
        }
        return json_interface

    @staticmethod
    def from_json(json_interface):
        if_name = json_interface.get('if_name')
        if_desc = json_interface.get('if_desc')
        protocol = json_interface.get('protocol')
        method = json_interface.get('method')
        url = json_interface.get('url')
        autotest = json_interface.get('autotest')
        system_id = json_interface.get('system_id')
        project_id = json_interface.get('project_id')
        if if_name is None or if_name == '':
            raise ValidationError('if_name is null')
        if project_id is None or project_id == '':
            raise ValidationError('project_id is null')
        if system_id is None or system_id == '':
            raise ValidationError('system_id is null')
        if url is None or url == '':
            raise ValidationError('url is null')
        return Interface(if_name=if_name, if_desc=if_desc, protocol=protocol, method=method, url=url,
                         autotest=autotest, system_id=system_id, project_id=project_id)


class Caserefer(db.Model):
    __tablename__ = 'caserefers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mockid = db.Column(db.Integer, db.ForeignKey('testcases.id'))
    refer_mockid = db.Column(db.Integer, db.ForeignKey('testcases.id'))
    ordernum = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    mock = db.relationship('Testcase', back_populates='caserefers', foreign_keys=[mockid])
    refer_mock = db.relationship('Testcase', back_populates='casemockrefers', foreign_keys=[refer_mockid])

    def to_json(self):
        json_caserefer = {
            'id': self.id,
            'mockid': self.mockid,
            'refer_mockid': self.refer_mockid,
            'ordernum': self.ordernum,
            'timestamp': self.timestamp
        }
        return json_caserefer

    @staticmethod
    def from_json(json_caserefer):
        mockid = json_caserefer.get('mockid')
        refer_mockid = json_caserefer.get('refer_mockid')
        ordernum = json_caserefer.get('ordernum')
        if mockid is None or mockid == '':
            raise ValidationError('mockid is null')
        if refer_mockid is None or refer_mockid == '':
            raise ValidationError('refer_mockid is null')
        if ordernum is None or ordernum == '':
            raise ValidationError('ordernum is null')
        return Caserefer(mockid=mockid, refer_mockid=refer_mockid, ordernum=ordernum)

class Testcase(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(64))
    interface_id = db.Column(db.Integer, db.ForeignKey('interfaces.id'))
    request_json = db.Column(db.Text)
    request_head = db.Column(db.Text)
    url = db.Column(db.String(128))
    response_json = db.Column(db.Text)
    response_head = db.Column(db.Text)
    check_json = db.Column(db.Text)
    ref_json = db.Column(db.Text)
    is_case = db.Column(db.Boolean, default=1)
    status = db.Column(db.Boolean, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    caserefers = db.relationship('Caserefer', back_populates='mock',foreign_keys=[Caserefer.mockid])
    casemockrefers = db.relationship('Caserefer', back_populates='refer_mock', foreign_keys=[Caserefer.refer_mockid])

    def to_json(self):
        json_testcase = {
            'id': self.id,
            'case_name': self.case_name,
            'interface_id': self.interface_id,
            'request_json': json.loads(self.request_json),
            'request_head': json.loads(self.request_head),
            'url': self.url,
            'response_json': json.loads(self.response_json),
            'response_head': json.loads(self.response_head),
            'check_json': json.loads(self.check_json),
            'ref_json': json.loads(self.ref_json),
            'is_case': self.is_case,
            'status': self.status,
            'timestamp': self.timestamp
        }
        return json_testcase

    @staticmethod
    def from_json(json_testcase):
        case_name = json_testcase.get('case_name')
        interface_id = json_testcase.get('interface_id')
        request_json = json.dumps(json_testcase.get('request_json'))
        request_head = json.dumps(json_testcase.get('request_head'))
        url = json_testcase.get('url')
        response_json = json.dumps(json_testcase.get('response_json'))
        response_head = json.dumps(json_testcase.get('response_head'))
        check_json = json.dumps(json_testcase.get('check_json'))
        ref_json = json.dumps(json_testcase.get('ref_json'))
        if case_name is None or case_name == '':
            raise ValidationError('case_name is null')
        return Testcase(case_name=case_name, interface_id=interface_id, request_json=request_json, request_head=request_head,
                   url=url, response_json=response_json, response_head=response_head,
                   check_json=check_json, ref_json=ref_json)

class Caseextract(db.Model):
    __tablename__ = 'caseextracts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mockid = db.Column(db.Integer, db.ForeignKey('testcases.id'))
    extract_name = db.Column(db.String(128))
    extract_value = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        json_caseextract = {
            'id': self.id,
            'mockid': self.mockid,
            'extract_name': self.extract_name,
            'extract_value': self.extract_value,
            'timestamp': self.timestamp
        }
        return json_caseextract

    @staticmethod
    def from_json(json_caseextract):
        mockid = json_caseextract.get('mockid')
        extract_name = json_caseextract.get('extract_name')
        extract_value = json_caseextract.get('extract_value')
        if mockid is None or mockid == '':
            raise ValidationError('mockid is null')
        if extract_name is None or extract_name == '':
            raise ValidationError('extract_name is null')
        if extract_value is None or extract_value == '':
            raise ValidationError('extract_value is null')
        return Caseextract(mockid=mockid, extract_name=extract_name, extract_value=extract_value)

class Assertrule(db.Model):
    __tablename__ = 'assertrules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mockid = db.Column(db.Integer, db.ForeignKey('testcases.id'))
    assert_type = db.Column(db.String(64))
    exp_value = db.Column(db.String(128))
    act_value = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        json_assertrule = {
            'id': self.id,
            'mockid': self.mockid,
            'assert_type': self.assert_type,
            'exp_value': self.exp_value,
            'act_value': self.act_value,
            'timestamp': self.timestamp
        }
        return json_assertrule

    @staticmethod
    def from_json(json_assertrule):
        mockid = json_assertrule.get('mockid')
        assert_type = json_assertrule.get('assert_type')
        exp_value = json_assertrule.get('exp_value')
        act_value = json_assertrule.get('act_value')
        if mockid is None or mockid == '':
            raise ValidationError('mockid is null')
        if assert_type is None or assert_type == '':
            raise ValidationError('assert_type is null')
        if exp_value is None or exp_value == '':
            raise ValidationError('exp_value is null')
        if act_value is None or act_value == '':
            raise ValidationError('act_value is null')
        return Assertrule(mockid=mockid, assert_type=assert_type, exp_value=exp_value, act_value=act_value)

class Testresult(db.Model):
    __tablename__ = 'testresults'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey('testcases.id'))
    test_result = db.Column(db.String(10))
    real_rsp_code = db.Column(db.String(20))
    real_req_path = db.Column(db.String(256))
    real_req_head = db.Column(db.Text)
    real_req_json = db.Column(db.Text)
    real_rsp_head = db.Column(db.Text)
    real_rsp_json = db.Column(db.Text)
    real_rsp_time = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        json_testresult = {
            'id': self.id,
            'case_id': self.case_id,
            'test_result': self.test_result,
            'real_rsp_code': self.real_rsp_code,
            'real_req_path': self.real_req_path,
            'real_req_head': json.loads(self.real_req_head),
            'real_req_json': json.loads(self.real_req_json),
            'real_rsp_head': json.loads(self.real_rsp_head),
            'real_rsp_json': json.loads(self.real_rsp_json),
            'real_rsp_time': self.real_rsp_time,
            'timestamp': self.timestamp
        }
        return json_testresult