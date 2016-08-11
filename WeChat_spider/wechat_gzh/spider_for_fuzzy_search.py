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
            'ABTEST': '0|1469412044|v1',
            'SNUID': '893EA94B9294AAFDB77B7FDE926A6AAB',
            'IPLOC': 'CN3700',
            'SUID': '18AC3BDA433E900A00000000579572CC',
            'JSESSIONID': 'aaadvUENQmZQYe-rf6Pxv',
            'SUV': '1469412047751761',
            'weixinIndexVisited': '1',
            'sct': '4',
            'ppinf': '5|1469501867|1470711467|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxMTppJUUyJTgwJTg2b3xjcnQ6MTA6MTQ2OTUwMTg2N3xyZWZuaWNrOjExOmklRTIlODAlODZvfHVzZXJpZDo0NDo4M0JEMzQ5QUE4QUE5MTlBMzFENjUyMUM1Q0IyRDAxRkBxcS5zb2h1LmNvbXw',
            'pprdig': 'lM6Ym9QoLOesylGeaS5w8B7nz2XyVdAEmLf4mTg7EAY61vjFJQi3f_E20yG4UsK0Ifx2yXNE7rjK1wbkQQI9G0LW4d_Q8MKmg0B1KODSLkzJw2_0UQRpIhz0YTBQs6pkBbdVOhOsRAX7VimSh5TXRL8krfsXkysfhg7FzqvOFfQ',
            'ppmdig': '14695018670000008f623b041a9ba269ad4843f719b36d3c',
            'PHPSESSID': '8g0c1nf9v59uluglmgc4dmnk25',
            'SUIR': '893EA94B9294AAFDB77B7FDE926A6AAB',
            'sucessCount': '1|Tue, 26 Jul 2016 03:48:00 GMT',
            'LSTMV': '513 % 2C137',
            'LCLKINT': '33357'
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
        _name = []
        _id = []
        name_id_list = []
        # for key_word in self.kws:

        for i in range(1):
            print('wwww')
            # wechat_search_url = self.host + self.keyword + '&page=' + str(i)
            wechat_search_url = self.host + '钓鱼' + '&page=' + str(i)
            print(wechat_search_url)
            print('page='+str(i))
            try:
                r = requests.get(wechat_search_url, headers=self.headers, cookies=self.cookies)
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


