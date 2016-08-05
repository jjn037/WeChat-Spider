"""WeChat_spider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from wechat_gzh import views
from WeChat_spider import settings
import os

urlpatterns = [
    url(r'article/update/gzh', views.articles_updated, name='gzh_updated'),
    url(r'article/update/article', views.gzh_updated, name='articles_updated'),
    url(r'article/new/(?P<gzh_id>[\w\-]+)$', views.new_articles, name='new_article'),
    url(r'article/add_gzh', views.add_gzh, name='add_gzh'),
    url(r'article/content/(?P<id>[\w\-]+)$', views.article_content, name='article_content'),
    url(r'^admin/', admin.site.urls),
    url(r'^article/(?P<gzh_id>[\w\-]+)$', views.article, name='article_list'),

    url(r'', views.index, name='index'),
    url(r'^images/(?P<path>.*)', 'django.views.static.serve',
        {'document_root': os.path.join( settings.STATIC_PATH, 'images')}),

]
