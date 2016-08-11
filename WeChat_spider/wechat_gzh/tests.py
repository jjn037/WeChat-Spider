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

def a():
    return {'q':1,'w':2}

b=a()
print(b['q'])
