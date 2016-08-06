from django.conf.urls import url
from django.contrib import admin
from wechat_gzh import views
from WeChat_spider import settings
import os

urlpatterns = [
    url(r'update/gzh', views.gzh_updated, name='gzh_updated'),
    url(r'update/article', views.articles_updated, name='articles_updated'),
    url(r'new/(?P<gzh_id>[\w\-]+)$', views.new_articles, name='new_article'),
    url(r'add_gzh', views.add_gzh, name='add_gzh'),
    url(r'content/(?P<id>[\w\-]+)$', views.article_content, name='article_content'),

    url(r'(?P<gzh_id>[\w\-]+)$', views.article, name='article_list'),
    url(r'', views.index, name='index'),
    # url(r'^images/(?P<path>.*)', 'django.views.static.serve',
    #     {'document_root': os.path.join(settings.STATIC_PATH, 'images')}),

]