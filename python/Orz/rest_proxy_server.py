import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options


from tornado.options import define,options

define('port' , default=8989 , help="mysql proxy server's port ~" , type = int)

class RESTProxyHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

def main():
    '''mysql proxy server action ~'''
    tornado.options.parse_command_line()
    application = tornado.web.Application([(r"/" , RESTProxyHandler),])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port , '127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

