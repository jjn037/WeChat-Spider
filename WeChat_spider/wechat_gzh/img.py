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

for i in range(10):

    article_list = Article.objects.filter(gzh__weixin_id__exact='changchundiaoyu')[i]
    today = time.strftime('%Y-%m-%d')
    if article_list.publish_date == today:
# for a in article_list.publish_date:
#     print(a)


       print(article_list.title)
    else:
        print(today)

#
# aa = GZH.objects.all()
# for a in aa:
#     print(a.weixin_id)
# bb = Article.objects.filter(gzh__weixin_id__exact='changchundiaoyu')
# for b in bb:
#     print(b.publish_date)
#     print(b.title)
