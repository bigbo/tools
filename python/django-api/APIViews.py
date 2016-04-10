# -*- coding: utf-8 -*-
from django import http
import json
from django.views.generic import View
from Exceptions import APIError
import time
import uuid

class JSONResponse(object):
    '''
    返回json对象统一封装
    '''

    def success(self, context):
        data = {
                'code': 0,
                'data': context
                }
        return self.render_to_response(data)

    def fail(self, code, message):
        data = {
                'code': code,
                'message': message
                }

        return self.render_to_response(data)

    def invalid(self):
        return self.fail(-1001, u'无效请求')

    def render_to_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        '''
        构造httpresponse对象
        '''
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)


class CoreView(JSONResponse, View):
    '''
    所有API基类
    '''

    def create_id(self):
        '''
        生成全局唯一id
        '''
        t = int(time.time()*1000)
        mac = int(uuid.UUID(int=uuid.getnode()).hex[-12:], 16)
        return t + mac

    def parameters(self, key):
        '''
        获取POST或者GET中的参数,POST参数如获取不到默认返回''
        '''
        if self.request.method == 'GET':
            return self.request.GET.get(key)
        if self.request.method == 'POST':
            if key in json.loads(self.request.body.decode()):
                return json.loads(self.request.body.decode()).get(key)
            else:
                return ''

    def url_parameters(self, key):
        return self.kwargs.get(key)

    def get(self, request, *args, **kwargs):
        '''
        收到GET请求后的处理
        '''

        self.args = args
        self.kwargs = kwargs
        if 'action' not in kwargs:
            return JSONResponse.invalid(self)

        action = 'get_%s' % kwargs['action'].lower()
        return self.run(action, request)

    def post(self, request, *args, **kwargs):
        '''
        收到POST请求后的处理
        '''

        self.args = args
        self.kwargs = kwargs
        if 'action' not in kwargs:
            return JSONResponse.invalid(self)

        action = 'post_%s' % kwargs['action'].lower()

        return self.run(action, request)

    def run(self, action, request):
        '''
        执行相应的逻辑
        '''
        self.request = request

        try:
            func = getattr(self, action)
        except:
            return JSONResponse.invalid(self)

        try:
            context = func()
        except APIError, e:
            return JSONResponse.fail(self, e.code, e.message)

        return JSONResponse.success(self, context)
