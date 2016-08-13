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


article_list = Article.objects.filter(gzh__weixin_id__exact='diao--yu')
grouped_articles = {}
for article in article_list:
    articles = grouped_articles.get(article.publish_date) or []
    articles.append(article)
    grouped_articles[article.publish_date] = articles

print(grouped_articles)