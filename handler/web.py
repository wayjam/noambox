from tornado import web, websocket
import os.path
import time
from handler.config import data, logger
from handler.controller import Controller
from handler import maps

'''
Web Handler
'''


class DemoHandler(web.RequestHandler):

    def get(self):
        self.render('demo.html')


class PlayHandler(web.RequestHandler):

    def get(self):
        self.render('play.html')


class FmHandler(web.RequestHandler):

    def get(self):
        self.render('fm.html',
                    webtitle='Fm')


class SettingHandler(web.RequestHandler):

    def get(self):
        self.render('setting.html',
                    webtitle='Setting',
                    douban_account=data.history.douban,
                    config_set=data.config
                    )

    def post(self):
        data.config.scroll_lryic = bool(self.get_arguments('scroll_lryic'))
        data.config.enable_rpc = bool(self.get_arguments('enable_rpc'))
        data.config.use_netease_source = bool(self.get_arguments(
            'use_netease_source'))
        data.save('config')
        self.render('setting.html',
                    webtitle='Setting',
                    douban_account=data.history.douban,
                    config_set=data.config
                    )


class InfoHandler(web.RequestHandler):

    def get(self):
        self.render('info.html')

'''
Websocket api
'''

browser = []


def sendmsg(message):
    for b in browser:
        b.write_message(message)


class ApiHandler(websocket.WebSocketHandler):

    def open(self):
        if self not in browser:
            browser.append(self)

    def on_message(self, message):
        result = maps.manager(message)
        return_msg = {
            'time': int(time.time() * 1000),
            'command': result[0],
            'content': result[1]
        }
        sendmsg(return_msg)

    def on_close(self):
        if self in browser:
            browser.remove(self)


'''
UI Module
'''


class SetboxModule(web.UIModule):

    def render(self, name, text, type, value=''):
        return self.render_string('modules/setbox.html', name=name, text=text, type=type, value=value)

'''
web.application
'''


class Application(web.Application):

    def __init__(self):
        handlers = [
            (r'/', PlayHandler),
            (r'/fm', FmHandler),
            (r'/setting', SettingHandler),
            (r'/info', InfoHandler),
            (r'/api', ApiHandler),
            (r'/demo', DemoHandler)

        ]
        settings = dict(
            template_path=os.path.join(
                os.path.dirname(__file__), "../templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../static"),
            ui_modules={
                'Setbox': SetboxModule
            },
            debug=True,
        )
        web.Application.__init__(self, handlers, **settings)
