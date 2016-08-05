# -*- coding:utf-8 -*-
import requests, re, urllib.request
from bs4 import BeautifulSoup
from time import sleep
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeChat_spider.settings')

import django, time

django.setup()

from wechat_gzh.models import GZH, Article

_gzhs = []
gzh_dict = {}

i =0



for k in range(10000):
    # try:
    #     i = i + 1
    #     gzhs = GZH.objects.all()[i]
    #     print(gzhs.weixin_id)
    # except:
    #     break
    # gzh_id = gzhs.weixin_id
    try:
        article = Article.objects.all()[k]
        print(article.title)
        today = time.strftime('%Y-%m-%d')
        print('today='+today)
        if article.publish_date != today:
            # gzh_updated = article.gzh.weixin_id
            # print('update='+gzh_updated)
            _gzhs.append(article)

    except:
        pass

for gzh in _gzhs:
    print('title='+gzh.title)
print("ok")