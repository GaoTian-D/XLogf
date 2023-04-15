#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: api.py
- date: 30/01/2023
"""

from flask import (
    Blueprint, request, render_template, make_response, Response, session
)
from flask_cors import CORS
from functools import wraps
from flask import jsonify, redirect
from flask import current_app
from flask_app import redis_client
from flask_app.utils.func import random_prefix_generator

'''
api 视图
'''
bp = Blueprint('api', __name__, url_prefix='/xlogf')

cors = CORS(bp, resources={
    r"/xlogf/*": {"origins": "*", "supports_credentials": True, "methods": ['GET', 'POST']},
})


def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if '_expires' not in session:
            return redirect("/xlogf/index.html")
        return f(*args, **kwargs)

    return decorated_function


@bp.route('/getdomain.php', methods=['GET'])
@session_required
def getdomain():
    '''
    todo. 调用频率限制
    :return:
    '''
    try:
        prefix = random_prefix_generator()
        if redis_client.exists('xlogf:domain:temporary:%s' % prefix) or redis_client.exists(
                'xlogf:domain:persistent:%s' % prefix):
            return Response("已经存在, 请重新尝试!", status=200, content_type='text/html; charset=utf-8')
        else:
            key = 'xlogf:domain:temporary:%s' % prefix
            redis_client.rpush(key, 'placeholder')
            redis_client.expire(key, current_app.config['DOMAIN_EXPIRE'])
            session['prefix'] = prefix
            temporary_domain = '%s.%s (有效剩余时间 %d 分钟)' % (
                prefix, current_app.config['DOMAIN_SUPPFIX'], current_app.config['DOMAIN_EXPIRE'] / 60)
            return Response(temporary_domain, status=200, content_type='text/html; charset=utf-8')
    except:
        return Response("Exception!", status=200, content_type='text/html; charset=utf-8')


@bp.route('/getrecords.php', methods=['GET'])
@session_required
def getrecords():
    if 'prefix' in session and session['prefix']:
        records = []
        try:
            key = 'xlogf:domain:temporary:%s' % session['prefix']
            if redis_client.exists(key):
                '''
                限制 1024
                '''
                for v in redis_client.lrange(key, 0, 1024):
                    if v.decode('utf-8') == 'placeholder':
                        # 去掉占位符
                        continue
                    message = v.decode('utf-8').split(',')
                    if len(message) == 4:
                        # ['xdzm14.sup0rnm4n.com', ' A', '127.0.0.1:57739', ' 2023-01-31 14:22:23']
                        records.append([message[0].strip(), message[2].strip(), message[3].strip()])
        except:
            pass
        return jsonify(records)
    else:
        return jsonify([])


@bp.route('/', methods=['GET'])
def index():
    if 'prefix' in session:
        prefix = session['prefix']
        if prefix:
            key = 'xlogf:domain:temporary:%s' % prefix
            ttl = redis_client.ttl(key)
            if ttl == -2:
                session['prefix'] = None
            else:
                if ttl / 60 > 1:
                    msg = '%s.%s (有效剩余时间 %d 分钟)' % (prefix, current_app.config['DOMAIN_SUPPFIX'], ttl / 60)
                else:
                    msg = '%s.%s (有效剩余时间 %d 秒)' % (prefix, current_app.config['DOMAIN_SUPPFIX'], ttl)
                return render_template('index.html', message=msg)
    else:
        # 为新的来访者生成会话
        session['prefix'] = None
        session.permanent = False

    return render_template('index.html', message=None)
