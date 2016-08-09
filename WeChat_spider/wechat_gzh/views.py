from django.shortcuts import render, render_to_response, RequestContext
from wechat_gzh.models import GZH, Article
from wechat_gzh.forms import GZHForm
from wechat_gzh.add_gzh import WXGZH
from django.template import RequestContext
import time, datetime
import json


def index(request):
    gzh_list = GZH.objects.all()
    gzh_dict = {'gzhs': gzh_list}

    return render_to_response('index.html', gzh_dict)


# def article(request, gzh_id):
#     article_list = Article.objects.filter(gzh__weixin_id__exact=gzh_id)
#
#     article_dict = {'articles': article_list}
#
#     return render_to_response('article_list.html', article_dict)
def article(request, gzh_id):
    rows = 0
    article_list = Article.objects.filter(gzh__weixin_id__exact=gzh_id)[0:]
    grouped_articles = {}
    for article in article_list:
        rows += 1
        articles = grouped_articles.get(article.publish_date) or []
        articles.append(article)
        grouped_articles[article.publish_date] = articles

    sorted_articles = sorted(grouped_articles.items(), reverse=True)
    article_context = {'date_articles': sorted_articles}

    return render_to_response('article_list.html', article_context)

'''
list = [
    {'date': date_str1, 'articles': [article1, article2]},
    {'date': date_str2, 'articles': articl_list},
    {'date': date_str3, 'articles': articl_list}
]
'''

def article_content(request, id):
    # content_dict = {}
    article = Article.objects.filter(id=id)[:1]
    content_dict = {'contents': article}

    return render_to_response('article_content.html', content_dict)


def add_gzh(request):
    if request.method == 'POST':
        form = GZHForm(request.POST)
        # print(dir(form))
        if form.is_valid():
            # form.save()
            id = form.cleaned_data['weixin_id']
            gzh = WXGZH(id)
            gzh.gzh_info_list()
            return index(request)
        else:
            print(form.errors)
    else:
        form = GZHForm()
    return render_to_response('add_gzh.html', {'form': form}, context_instance=RequestContext(request))


def new_articles(request, gzh_id):
    today_articles_dic = {}
    new_article = []
    try:
        article_list = Article.objects.filter(gzh__weixin_id__exact=gzh_id)[0:]
        today = time.strftime('%Y-%m-%d')
        for article in article_list:
            if article.publish_date == today:
                new_article.append(article_list)
                gzh_updated = article_list.gzh.weixin_id
                # today_articles_dic['gzh_updated']
                today_articles_dic = {'new_articles': new_article}
    except:
        pass
    return render_to_response('today.html', today_articles_dic)


def gzh_updated(request):
    gzh_dict = {}
    _gzhs = []
    try:
        gzhs_list = GZH.objects.all()[0:]
    except:
        pass
    for gzhs in gzhs_list:
        gzh_id = gzhs.weixin_id
        try:
            article = Article.objects.filter(gzh__weixin_id__exact=gzh_id)[0]
            print(article.title)
            today = time.strftime('%Y-%m-%d')
            print('today=' + today)
            if article.publish_date == today:
                gzh_updated = article.gzh.weixin_id
                print('update=' + gzh_updated)
                _gzhs.append(article)
        except:
            pass
    gzh_dict['gzhs'] = _gzhs

    return render_to_response('gzh_update.html', gzh_dict)


def articles_updated(request):
    _article = []

    try:
        article_list = Article.objects.all()[0:]
        for article in article_list:
            print(article.title)
            today = time.strftime('%Y-%m-%d')
            print('today=' + today)
            if article.publish_date == today:
                # gzh_updated = article.gzh.weixin_id
                # print('update='+gzh_updated)
                _article.append(article)

    except:
        pass

    article_updated_dict = {'articles': _article}
    return render_to_response('articles_updated.html', article_updated_dict)

