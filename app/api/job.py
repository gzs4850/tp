#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/2 15:00
# @Author  : z.g

from . import api
from .. import scheduler
from flask import request
import json

@api.route('/jobpause', methods=['POST'])
def pause_job():
    response = {'code': '-1'}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        scheduler.pause_job(job_id)
        response['msg'] = "job [%s] pause success!" %job_id
        response['code'] = 1
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

@api.route('/jobresume', methods=['POST'])
def resume_job():
    response = {'code': '-1'}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        scheduler.resume_job(job_id)
        response['msg'] = "job [%s] resume success!" %job_id
        response['code'] = 1
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

@api.route('/jobremove', methods=['DELETE'])
def remove_job():
    response = {'status': "-1"}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        scheduler.remove_job(job_id)
        response['msg'] = "job [%s] remove success!" %job_id
        response['status'] = 1
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

@api.route('/jobedit', methods=['POST'])
def edit_job():
    response = {'code': "-1"}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        old_job = scheduler.get_job(job_id)
        if old_job:
            jobfromparm(**data)
            response['msg'] = "job [%s] edit success!" % job_id
            response['code'] = 1
        else:
            response['msg'] = "job [%s] Not Found!" %job_id
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

@api.route('/jobadd', methods=['POST'])
def add_job():
    response = {'code': "-1"}
    try:
        data = request.get_json(force=True)
        # job_id = data.get('id')
        job_id = jobfromparm(**data)
        response['msg'] = "job [%s] add success!" %job_id
        response['code'] = 1
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

def show_jobs():
    response = {}
    try:
        jid = request.args.get('id')
        if jid == None:
            ret_list = scheduler.get_jobs()
        else:
            ret_list = [scheduler.get_job(jid)]
        info_list = []
        for ret in ret_list:
            fields = ret.trigger.fields
            cron = {}
            for field in fields:
                cron[field.name] = str(field)
            cron_list = [cron['second'],cron['minute'],cron['hour'],cron['day'],cron['month'],cron['day_of_week']]
            info = {
                'id': ret.id,
                'next_run_time': ret.next_run_time,
                'cmd': ret.kwargs.get('cmd'),
                # 'func':ret.func_ref,
                'status': 'running' if ret.next_run_time != None else 'stop',
                'cron': ' '.join(cron_list)
            }
            info_list.append(info)
        response['code'] = 1
        response['data'] = info_list
        response['count'] = len(info_list)
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

def exe_cmd(cmd,task_id):
    print("hello %s %s" %(cmd,task_id))

def jobfromparm(**jobargs):
    id = jobargs['id']
    func = __name__+':'+'exe_cmd'
    args = jobargs['cmd']
    cron = jobargs['cron'].split(' ')
    cron_rel = dict(second=cron[0], minute=cron[1], hour=cron[2], month=cron[4], day_of_week=cron[5])
    print(cron_rel)
    scheduler.add_job(func=func, id=id, kwargs={'cmd': args, 'task_id': id}, trigger='cron', **cron_rel, replace_existing=True)
    print(id)
    return id
