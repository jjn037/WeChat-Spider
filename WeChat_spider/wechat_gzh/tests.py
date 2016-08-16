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
a = open('../cookies.txt').read()

# print(a)

_cookies={}
aa = a.replace('\r', '').replace('\n', '').split(';')
a.close()
# print(aa)
# print(len(aa))
for b in aa:
    c = b.split('=')
    # print(c)
    # print(len(c))
    #
    # print(c[0])
    _cookies[c[0]] = c[1]
print(_cookies)
# a1 = (str(aa).split('='))
# for aaa in a1:
#     a2 = str(aaa).split(',')
#     for a3 in a2:
#         a4 = a3.replace('\'', '')
#         print(a4)

    # c = str(b)
    # for d in c:
    #     print(d)
    # print(c.split())
    # print(type(c))

#
# #     for b in aaa:
# #         print(b)
# #     _cookies.append(aaa)
# # print(_cookies)
#
# cookies = a.replace('=', '\' : \'').replace('\n', '').split(';')
# for cook in cookies:
#     cookies_format = ('\''+cook.strip()+'\'')
#     _cookies.append(cookies_format)
# print((_cookies))
#
#
