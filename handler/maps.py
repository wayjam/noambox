from api import doubanfm
import model
import json

'''
FM
'''
fm = doubanfm.FM()


def manager(msg):
    parse_msg = json.loads(msg)
    switcher = {
        'douban_captcha': douban_captcha,
        'douban_login': douban_login,
        'douban_fav_channels': douban_fav_channels,
        'douban_hot_channels': douban_hot_channels,
        'douban_up_trending_channels': douban_up_trending_channels,
        'douban_recommended_channel_list': douban_channel_list,
        'douban_search_channel': douban_search_channel
    }
    func = switcher.get(parse_msg['command'], lambda: "nothing")
    return func(parse_msg['content'])


def douban_captcha(args):
    return "douban_captcha", fm.captcha_id(True)


def douban_login(args):
    return "douban_login", fm.login(args['username'], args['password'], args['captcha_solution'], args['captcha_id'])


def douban_fav_channels(args):
    return "douban_fav_channels",fm.fav_channel_list()


def douban_hot_channels(args):
    return fm.douban_hot_channels(start=args['start'], limit=args['limit'])


def douban_up_trending_channels(args):
    return fm.up_trending_channels(start=args['start'], limit=args['limit'])


def douban_recommended_channel_list(args):
    return fm.channel_list()


def douban_search_channel(args):
    return fm.search_channel(keyword=args['keyword'], start=args['start'], limit=args['limit'])
