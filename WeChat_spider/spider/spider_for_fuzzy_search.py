#!/bin/env /usr/local/bin/python3
# coding: utf-8
import requests, re, urllib.request
from bs4 import BeautifulSoup
from time import sleep
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeChat_spider.settings')

import django

django.setup()

from wechat_gzh.models import GZH, Article


class Wechat_gzh_fuzzy_search:
    def __init__(self, key_words):
        self.kws = key_words
        self.host = 'http://weixin.sogou.com/weixin?type=1&query='
        self.gzh_info = []
        self.cookies = {

        }
        self.headers = {
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep - alive',
            'Host': 'weixin.sogou.com',
            'Referer': 'http://weixin.sogou.com/weixin?query=%E9%92%93%E9%B1%BC&_sug_type_=&sut=2960&lkt=2,1469418101779,1469418103662&_sug_=y&type=1&sst0=1469418103770&page=1&ie=utf8&w=01019900&dr=1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
        }

    def gzh_info_list(self):
        cookies_raw = open('../cookies.txt').read()
        _cookies_raw = cookies_raw.replace('\r', '').replace('\n', '').split(';')

        for _cookies in _cookies_raw:
            coolies = _cookies.split('=')
            self.cookies[coolies[0]] = coolies[1]
        name_id_list = []
        # for key_word in self.kws:

        for i in range(1, 10):
            print('wwww')
            for key_word in self.kws:
                # wechat_search_url = self.host + self.keyword + '&page=' + str(i)
                wechat_search_url = self.host + key_word + '&page=' + str(i)
                print(wechat_search_url)
                print('page='+str(i))
                try:
                    r = requests.get(wechat_search_url, headers=self.headers)  ###
                except:
                    pass
                sleep(5)
                soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")
                for items in soup.findAll('div', {'class': 'wx-rb'}):
                    name = items.find('h3').text
                    # _name.append(name)
                    print('name='+name)
                    wx_id = items.find('label').text
                    # _id.append(wx_id)
                    name_id_dict = {'name': name, 'id': wx_id}
                    name_id_list.append(name_id_dict)

            return {'names_ids': name_id_list}


