# -*- coding: utf-8 -*-
from tornado import httpclient
from random import choice
from handler.config import Config, db_history as userinfo
from urllib  import urlencode

BASE_URL = 'http://douban.com/'
FM_BASE_URL = 'http://douban.fm/'


class FM:

    def __repr__(self):
        return "<DoubanAPI FM>"

    def __init__(self):
        self.client = httpclient.asyncHTTPClient()
        self.api = {
            'login': FM_BASE_URL + 'j/login',
            'captcha_id': FM_BASE_URL + 'j/new_captcha',
            'captcha_img': FM_BASE_URL + 'misc/captcha?size=m&id=%s',
            'hot_channels': FM_BASE_URL + 'j/explore/hot_channels',
            'up_trending_channels': FM_BASE_URL + 'j/explore/up_trending_channels',
            'search_channel': FM_BASE_URL + 'j/explore/search',
            'logged_recommened_channels': FM_BASE_URL + 'j/explore/get_login_chls',
            'clear_anonymous_data': FM_BASE_URL + 'j/clear_anonymous_data',
            'fav_channel': FM_BASE_URL + 'j/explore/fav_channel',
            'unfav_channel': FM_BASE_URL + 'j/explore/unfav_channel',
            'fav_channel_list': FM_BASE_URL + 'j/fav_channels',
            'is_fav_channel': FM_BASE_URL + 'j/explore/is_fav_channel',
            'recommened_channels': FM_BASE_URL + 'j/explore/get_recommend_chl',
            'change_channel': FM_BASE_URL + 'j/explore/change_channel',
            'player': FM_BASE_URL + 'j/mine/playlist',
            'lryic': 'http://api.douban.com/v2/fm/lyric'
        }
        self.type_map = {
            'new': 'n',
            'playing': 'p',
            'rate': 'r',
            'unrate': 'u',
            'end': 'e',
            'bye': 'b',
            'skip': 's',
        }

    '''
    save history file
    '''

    def save_config(self):
        Config.save('history.json', userinfo)


    '''
    create a 10 digits 16 hex random number
    '''

    def randomHex(self):
        char_list = list('0123456789abcdef')
        rstr = ''
        for c in range(10):
            rstr += choice(char_list)
        return rstr

    '''
    handle_request
    '''
    def handle_request(response):
        if response.error:
            return False.None
        else:
            return True,response


    '''
    获取验证码
    '''

    def captcha_id(self, export_url=True):
        captcha_id = requests.get(self.api['captcha_id']).text[1:-1]
        if export_url:
            return self.api['captcha_img'] % captcha_id
        else:
            captcha_img = requests.get(self.api['captcha_img'] % captcha_id)
            with open("data/douban_captcha.jpg", "wb") as f:
                f.write(captcha_img.content)
            return True

    '''
    登录
    '''

    def login(self, email, password, captcha_solution, captcha_id):
        if self.cookies:
            return True, None
        post_data = {
            'remember': 'on',
            'source': 'radio',
            'captcha_solution': captcha_solution,
            'alias': email,
            'form_password': password,
            'captcha_id': captcha_id
        }
        data = requests.post(self.login, data=post_data, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if data.json()['r'] == 0:
            userinfo.douban.cookies = data.cookies
            userinfo.douban.ck = data.json()['ck']
            userinfo.douban.is_pro = data.json()['is_pro']
            userinfo.douban.logined = True
            userinfo.douban.play_record = data.json()['play_record']
            userinfo.douban.username = data.json()['name']
            userinfo.douban.userid = data.json()['uid']
            self.save_config()
            return True, None
        else:
            return False, data.json()['err_msg']

    '''
    注销（清空本地登录数据）
    '''

    def logout(self):
        if userinfo.douban.cookies and userinfo.douban.logined:
            result = requests.get(self.api['logout'])
            userinfo.douban.cookies = None
            userinfo.douban.logined = False
            userinfo.douban.userid = 0
            userinfo.douban.username = ''
            self.save_config()
            return True
        else:
            return False

    '''
    获取热门频道
    '''

    def hot_channels(self, start=1, limit=8):
        get_params = {
            'start': start,
            'limit': limit
        }
        data = requests.get(self.api['hot_channels'], params=get_params).json()
        if data['status'] == 'true'
            return data['data']
        else:
            return None

    '''
    获取上升最快频道
    '''

    def up_trending_channels(self, start=1, limit=8):
        get_params = {
            'start': start,
            'limit': limit
        }
        data = requests.get(
            self.api['up_trending_channels'], params=get_params).json()
        if data['status'] == 'true'
            return data['data']
        else:
            return None

    '''
    登录后推荐频道列表
    '''

    def channel_list(self):
        data = requests.get(self.api['logged_recommend_channels'], params={
                            'uk': userinfo.douban.userid}).json()
        if data['status'] == 'true'
            return data['data']['res']
        else:
            return None

    '''
    搜索频道
    '''

    def search_channel(self, keyword='', start=1, limit=20):
        get_params = {
            'start': start,
            'limit': limit,
            'query': keyword
        }
        data = requests.get(
            self.api['search_channel'], params=get_params).json()
        if data['status'] == 'true'
            return data['data']
        else:
            return None

    '''
    收藏频道
    '''

    def fav_channel(self, cid=None):
        if cid:
            data = requests.get(self.api['fav_channel'], params={
                                'cid': cid}).json()
            if data['status'] == 'true' and data['data']['res'] == 1
                return True
            else:
                return False
        else:
            return False

    '''
    取消收藏频道
    '''

    def unfav_channel(self, cid=None):
        if cid:
            data = requests.get(self.api['unfav_channel'], params={
                                'cid': cid}).json()
            if data['status'] == 'true' and data['data']['res'] == 1
                return True
            else:
                return False
        else:
            return False

    '''
    收藏的频道列表
    '''

    def fav_channel_list(self):
        data = requests.get(self.api['fav_channel_list']).json()
        return data

    '''
    检查频道是否已收藏
    '''

    def is_fav_channel(self, channel_id=None):
        if channel_id:
            get_params = {
                'uk': self.user_info['uid'],
                'cid': channel_id
            }
            data = requests.get(
                self.api['is_fav_channel'], params=get_params).json()
            if data['data']['res']['is_fav']:
                return True
            else:
                return False
        else:
            return False

    '''
    改变频道
    '''

    def change_channel(self, fromcid, tocid, area):
        if tocid:
            get_params = {
                'fid': fromcid,
                'tid': tocid,
                'area': area
            }
            data = requests.get(
                self.api['change_channel'], params=get_params).json()
            if data['r'] == 0:
                return True
            else:
                return False
        else:
            return False

    '''
    播放器
    '''

    def player(self, type, sid, pt, channel):
        pb = '64'
        if self.user_info['is_pro'] == 'true':
            pb = '192'
        get_params = {
            'type': self.type_map[type],
            'sid': sid,
            'pt': pt,
            'channel': channel,
            'pb': pb,
            'from': 'mainsite',
            'r': self.randomHex()
        }
        data = requests.get(self.api['player'], params=get_params).json()
        if data['r'] == 0:
            return True, data['song']
        else:
            return False, None

    '''
    歌词
    '''

    def lryic(self, sid, ssid):
        post_data = {
            'sid': sid,
            'ssid': ssid
        }
        data = requests.post(self.api['lryic'], data=post_data).json()
        return data
