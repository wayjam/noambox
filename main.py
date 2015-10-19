import os.path
from tornado import websocket,httpserver,ioloop,options,web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html');

def main():
    options.parse_command_line()
    app = web.Application(
            handlers=[
                (r'/', IndexHandler)
            ],
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
