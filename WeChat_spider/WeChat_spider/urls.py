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
from django.views import static

urlpatterns = [
    url(r'^article/cookies_change/', views.cookies_changed, name='cookies_changed'),
    url(r'article/update/gzh', views.gzh_updated, name='gzh_updated'),
    url(r'article/update/article', views.articles_updated, name='articles_updated'),
    # url(r'article/new/(?P<gzh_id>[\w\-]+)$', views.today_articles, name='new_article'),
    # url(r'article/add_gzh', views.add_gzh, name='add_gzh'),
    url(r'article/fuzzy_search_spider', views.fuzzy_search_spider, name='fuzzy_search_spider'),
    url(r'article/fuzzy_search', views.fuzzy_search, name='fuzzy_search'),

    url(r'article/content/(?P<id>[\w\-]+)$', views.article_content, name='article_content'),
    url(r'^admin/', admin.site.urls),
    url(r'^article/(?P<gzh_id>[\w\-]+)$', views.article, name='article_list'),
    url(r'^article/delete/', views.delete_id, name='delete_id'),

    url(r'', views.index, name='index'),


    url(r'^images/(?P<path>.*)', static.serve,
        {'document_root': os.path.join(settings.STATIC_PATH, 'images')}),

]
