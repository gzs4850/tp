# coding:utf-8
from flask import jsonify
from ..models import Testresult
from . import api
from .. import db

@api.route('/testresults/<int:id>')
def get_testresult(id):
    testresult = db.session.query(Testresult).filter(Testresult.case_id==id).first()

    if testresult:
        return jsonify({
            'code': 1,
            'testresult': testresult.to_json()
        })
    else:
        return jsonify({
            'code':1,
            'testresult':{}
        })