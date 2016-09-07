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



grouped_articles = {}
gzhs = GZH.objects.all()
for gzh in gzhs:
    article_list = Article.objects.filter(gzh__weixin_id__exact=gzh.weixin_id)[0:]
    if len(article_list)>0:

        articles = grouped_articles.get(article_list[0].publish_date) or []
        articles.append(gzh.name)
        grouped_articles[article_list[0].publish_date] = articles
sorted_articles = sorted(grouped_articles.items(), reverse=True)
for k, v in sorted_articles:
    print(k)
    print(v)


