# -*- coding: utf-8 -*-
from functools import wraps
from Exceptions import APIError
import json

def CheckParameters(fields=[], method='POST'):
    '''
    检查API参数函数，默认POST
    '''
    def wraps_decorator(f):
        @wraps(f)
        def check(self, *args, **kwargs):
            if method == 'POST':
                paraneters = json.loads(self.request.body.decode())
            if method == 'GET':
                paraneters = self.request.GET

            for field in fields:
                if field not in paraneters:
                    raise APIError(-1002)
            return f(self, *args, **kwargs)
        return check
    return wraps_decorator

