from django.test import TestCase

# Create your tests here.
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


# article_dict = {}
# _list = []
# _key = []
# _dict = {}
# _article = []
# l=0
# for i in range(10):
#     today = time.strftime('%Y,%m,%d')
#     a = datetime.datetime.now() + datetime.timedelta(-i)
#     day = a.strftime('%Y-%m-%d')
#     # print(day)
#
#     for k in range(100):
#         try:
#             article_list = Article.objects.filter(gzh__weixin_id__exact='ZHYL1666')[0:100]
#         except:
#             pass
#         # a = article_list.title
#         # print(a)
#
#         if article_list.publish_date == day:
#             if article_list.title not in _article:
#                 _article.append(article_list.title)
#                 if day not in _key:
#                     _key.append(day)
#                     _dict = {'date': day, 'title': _article}
#                     _list.append(_dict)
#
#
# for d in _list:
#     print(d['date'])
#         # print(d.ke)
#     for a in d['title']:
#         print(a)
article_list = Article.objects.filter(gzh__weixin_id__exact='ZHYL1666')[0:]
grouped_articles = {}
for article in article_list:
    articles = grouped_articles.get(article.publish_date) or []
    articles.append(article)
    grouped_articles[article.publish_date] = articles

# print(grouped_articles)
sorted_articles = sorted(grouped_articles.items())
print(sorted_articles[0][0])
