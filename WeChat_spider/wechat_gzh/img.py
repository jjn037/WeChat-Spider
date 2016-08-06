# -*- coding:utf-8 -*-
import requests, re, urllib.request
from bs4 import BeautifulSoup
from time import sleep
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeChat_spider.settings')

import django, time, datetime

django.setup()

from wechat_gzh.models import GZH, Article

articles = []
article_dict = {}
_list = []
_dict = {}

day = ''

today = time.strftime('%Y,%m,%d')
a = datetime.datetime.now() + datetime.timedelta(-1)

day = a.strftime('%Y-%m-%d')
print(type(day))

try:
    article = Article.objects.all()[0]

    if article.publish_date == day:

        articles = []
        for k in range(100):
            article_list = Article.objects.filter(gzh__weixin_id__exact='ZHYL1666')[k]

            if article_list.publish_date == day:

                print('article ok')
                article_dict.setdefault(day, []).append(article_list)
except:
    pass
_list.append(article_dict)
_dict = {'date': _list}
for date in _dict['date']:
    print(type(date))
    for art in date[day]:
        print(art.title)

