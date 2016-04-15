# -*- coding: utf-8 -*-
from random import choice
from handler.config import data
import requests

BASE_URL = 'http://douban.com/'
FM_BASE_URL = 'http://douban.fm/'


class FM:

    def __repr__(self):
        return "<DoubanAPI FM>"

    def __init__(self):
        self.client = requests.Session()
        self.cookies = ''
        self.api = {
            'login': FM_BASE_URL + 'j/login',
            'captcha_id': FM_BASE_URL + 'j/new_captcha',
            'captcha_img': FM_BASE_URL + 'misc/captcha?size=m&id=%s',
            'hot_channels': FM_BASE_URL + 'j/explore/hot_channels',
            'up_trending_channels': FM_BASE_URL + 'j/explore/up_trending_channels',
            'search_channel': FM_BASE_URL + 'j/explore/search',
            'logined_recommened_channels': FM_BASE_URL + 'j/explore/get_login_chls',
            'clear_anonymous_data': FM_BASE_URL + 'j/clear_anonymous_data',
            'fav_channel': FM_BASE_URL + 'j/explore/fav_channel',
            'unfav_channel': FM_BASE_URL + 'j/explore/unfav_channel',
            'fav_channel_list': FM_BASE_URL + 'j/fav_channels',
            'is_fav_channel': FM_BASE_URL + 'j/explore/is_fav_channel',
            'recommened_channels': FM_BASE_URL + 'j/explore/get_recommend_chl',
            'change_channel': FM_BASE_URL + 'j/change_channel',
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
        data.save('history.json')


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
            return False,None
        else:
            return True,response


    '''
    获取验证码
    '''

    def captcha_id(self, export_url=True):
        captcha_id = self.client.get(self.api['captcha_id']).text[1:-1]
        if export_url:
            return self.api['captcha_img'] % captcha_id
        else:
            captcha_img = self.client.get(self.api['captcha_img'] % captcha_id)
            with open("data.history/douban_captcha.jpg", "wb") as f:
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
        result = self.client.post(self.api['login'], data=post_data, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if result.json()['r'] == 0:
            self.cookies = result.cookies
            data.history.douban.ck = result.json()['user_info']['ck']
            data.history.douban.is_pro = result.json()['user_info']['is_pro']
            data.history.douban.logined = True
            data.history.douban.play_record = result.json()['user_info']['play_record']
            data.history.douban.username = result.json()['user_info']['name']
            data.history.douban.userid = result.json()['user_info']['uid']
            self.save_config()
            return True, None
        else:
            return False, result.json()['err_msg']

    '''
    注销（清空本地登录数据）
    '''

    def logout(self):
        if self.cookies and data.history.douban.logined:
            result = self.client.get(self.api['logout'])
            data.history.douban.cookies = None
            data.history.douban.logined = False
            data.history.douban.userid = 0
            data.history.douban.username = ''
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
        result = self.client.get(self.api['hot_channels'], params=get_params).json()
        if result['status'] == 'true':
            return result['data']
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
        result = self.client.get(
            self.api['up_trending_channels'], params=get_params).json()
        if result['status'] == 'true':
            return result['data']
        else:
            return None

    '''
    登录后推荐频道列表
    '''

    def channel_list(self):
        result = self.client.get(self.api['logined_recommened_channels'], params={
                            'uk': data.history.douban.userid}).json()
        if result['status'] == 'true':
            return result['data']['res']
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
        result = self.client.get(
            self.api['search_channel'], params=get_params).json()
        if result['status'] == 'true':
            return result['data.history']
        else:
            return None

    '''
    收藏频道
    '''

    def fav_channel(self, cid=None):
        if cid:
            result = self.client.get(self.api['fav_channel'], params={
                                'cid': cid}).json()
            if result['status'] == 'true' and result['data.history']['res'] == 1:
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
            result = self.client.get(self.api['unfav_channel'], params={
                                'cid': cid}).json()
            if result['status'] == 'true' and result['data.history']['res'] == 1:
                return True
            else:
                return False
        else:
            return False

    '''
    收藏的频道列表
    '''

    def fav_channel_list(self):
        result = self.client.get(self.api['fav_channel_list']).json()
        return result

    '''
    检查频道是否已收藏
    '''

    def is_fav_channel(self, channel_id=None):
        if channel_id:
            get_params = {
                'uk': data.history.douban.userid,
                'cid': channel_id
            }
            result = self.client.get(
                self.api['is_fav_channel'], params=get_params).json()
            if result['data']['res']['is_fav']:
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
            result = self.client.get(
                self.api['change_channel'], params=get_params).json()
            if result['r'] == 0:
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
        if data.history.douban.is_pro == True:
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
        result = self.client.get(self.api['player'], params=get_params).json()
        if result['r'] == 0:
            return True, result['song']
        else:
            return False, None

    '''
    歌词
    '''

    def lryic(self, sid, ssid):
        post_data.history = {
            'sid': sid,
            'ssid': ssid
        }
        result = self.client.post(self.api['lryic'], data=post_data).json()
        return result
