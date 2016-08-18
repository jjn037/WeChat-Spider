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


a = GZH.objects.filter(id=505)[0]
print(type(a.weixin_id))
if a.weixin_id == '':
    print('ok')

# url = 'http://mp.weixin.qq.com/s?timestamp=1471494102&src=3&ver=1&signature=KpwZRWbcCHlGkeTyqYlK8qHXhRU*JaCtsWz6hohtj*A8iLj0szwTtHlpzmN5iDF*6VhARlsqYxsx7eqna6fvzBsIWK1YTV49LEWrn*zPsFRu0NM92kbE2c1iwzqfTyKLCQsu8wCzCfYlFL5OyKmaXB99r-263-u5493Tr40xaDk='
#
url = 'http://weixin.sogou.com/weixin?type=1&query=钓竿&page=9'
r = requests.get(url=url)
print(r)
soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")
print(soup)