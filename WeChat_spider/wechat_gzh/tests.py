from django.test import TestCase

# Create your tests here.
# -*- coding:utf-8 -*-
import requests, re, urllib, urllib.request
from bs4 import BeautifulSoup
from time import sleep
import os
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeChat_spider.settings')
import django, time, datetime
django.setup()
from wechat_gzh.models import GZH, Article


# article_list = Article.objects.filter(gzh__weixin_id__exact='diao--yu')
# grouped_articles = {}
# for article in article_list:
#     articles = grouped_articles.get(article.publish_date) or []
#     articles.append(article)
#     grouped_articles[article.publish_date] = articles

# print(grouped_articles)
with open('../cookies.txt') as f:
    a = f.read()
# print(a)

_cookies={}
aa = a.replace('\r', '').replace('\n', '').split(';')
# a.close()
# print(aa)
# print(len(aa))
for b in aa:
    c = b.strip().split('=')
    # print(c)
    # print(len(c))
    #
    # print(c[0])
    _cookies[c[0]] = c[1]
print(_cookies)
#
# import random
# while 1:
#     a = random.randint(1, 10)
#     print(a)
#     sleep(a)