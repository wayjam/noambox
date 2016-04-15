# -*- coding: utf-8 -*-
import subprocess
from  multiprocessing import process
import os.path
from tornado import httpserver,ioloop,options

from handler import config,web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)


def main():
    config.logger.info("HttpServer Started.")
    options.parse_command_line()
    http_server = httpserver.HTTPServer(web.Application())
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
        main()
