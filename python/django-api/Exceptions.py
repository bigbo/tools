# -*- coding: utf-8 -*-

error_code_mapping = [
{'code':-1001, 'message':u'无效请求'},
{'code':-1002, 'message':u'参数错误'},
{'code':-1003, 'message':u'接口验证错误'},
{'code':-2000, 'message':u'未授权用户'},
{'code':-3000, 'message':u'没有找到相关信息'},
{'code':-4000, 'message':u'重复请求'},
{'code':-5000, 'message':u'未知错误'},
]

class APIError(Exception):

    def __init__(self, code, message=None):
        self.code = code

        if message is None:
            self.message = self.error_message
        else:
            self.message = message

    def __str__(self):
        return repr(self.code)

    @property
    def error_message(self):
        for item in error_code_mapping:
            if item['code'] == self.code:
                return item['message']

        return u'未知错误'