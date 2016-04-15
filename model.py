'''
Provide the Data Model
'''
import time


class Config(object):

    def __init__(self):
        self.play = Playing()
        self.use_netease_source = False
        self.scroll_lryic = False
        self.enable_rpc = False

class Playing(object):

    def __init__(self):
        self.title = ''
        self.singer = ''
        self.album = ''
        self.list = ''
        self.lryic = ''
        self.lengeth = 0
        self.pause = False
        self.time = 0
        self.volume = 50
        self.play_mode = 0
        self.stream = 0

class History(object):

    def __init__(self):
        self.last_time = int(time.time()*1000)
        self.run_time = 0
        self.douban = DoubanAccount()


class DoubanAccount(object):

    def __init__(self):
        self.ck = ''
        self.userid = ''
        self.is_pro = False
        self.username = ''
        self.play_record = {
            'banned': 0,
            'played': 0,
            'liked': 0,
            'fav_chls_count': 0
        }
        self.logined = False
        self.cookies = None
        self.channel_id = ''
        self.song_id = ''


class DoubanChannel(object):

    def __init__(self):
        self.intro = ''
        self.id = 0
        self.name = ''
        self.song_num = 0


class WsInteraction(object):

    def __init__(self):
        self.date = int(time.time()*1000)
        self.command = ''
        self.content = ''
