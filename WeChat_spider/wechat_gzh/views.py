import json
import time

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from spider.spider_add_gzh import Wechat_gzh
from spider.spider_for_fuzzy_search import Wechat_gzh_fuzzy_search
from wechat_gzh.models import GZH, Article


def index(request):
    _gzh_list = GZH.objects.all()

    paginator = Paginator(_gzh_list, 20)
    page = request.GET.get('page')
    try:
        gzh_list = paginator.page(page)
    except PageNotAnInteger:
        gzh_list = paginator.page(1)
    except EmptyPage:
        gzh_list = paginator.page(paginator.num_page)

    gzh_dict = {'gzhs': gzh_list}

    return render_to_response('index.html', gzh_dict)


def article(request, gzh_id):
    article_list = Article.objects.filter(gzh__weixin_id__exact=gzh_id)[0:]
    grouped_articles = {}
    for article in article_list:
        articles = grouped_articles.get(article.publish_date) or []
        articles.append(article)
        grouped_articles[article.publish_date] = articles

    sorted_articles = sorted(grouped_articles.items(), reverse=True)
    # article_context = {'date_articles': sorted_articles}
    paginator = Paginator(sorted_articles, 10)
    page = request.GET.get('page')
    try:
        article_context = paginator.page(page)
    except PageNotAnInteger:
        article_context = paginator.page(1)
    except EmptyPage:
        article_context = paginator.page(paginator.num_page)

    return render_to_response('article_list.html', {'date_articles': article_context})

'''
list = [
    {'date': date_str1, 'articles': [article1, article2]},
    {'date': date_str2, 'articles': articl_list},
    {'date': date_str3, 'articles': articl_list}
]
'''

def article_content(request, id):
    article = Article.objects.filter(id=id)[:1]
    content_dict = {'contents': article}

    return render_to_response('article_content.html', content_dict)


def fuzzy_search(request):
    if request.method == 'POST':
        # form = Fuzzy_search(request.POST)
        # if form.is_valid():
        #     key_words = form.cleaned_data['key']
        id = request.POST.getlist('weixin_id')
        wx = Wechat_gzh_fuzzy_search(id)
        fuzzy_info = wx.gzh_info_list()

        return render_to_response('fuzzy_search.html', fuzzy_info)


# def today_articles(request, gzh_id):
#     today_articles_dic = {}
#     new_article = []
#     try:
#         article_list = Article.objects.filter(gzh__weixin_id__exact=gzh_id)[0:]
#         today = time.strftime('%Y-%m-%d')
#         for article in article_list:
#             if article.publish_date == today:
#                 new_article.append(article_list)
#                 gzh_updated = article_list.gzh.weixin_id
#                 # today_articles_dic['gzh_updated']
#                 today_articles_dic = {'new_articles': new_article}
#     except:
#         pass
#     return render_to_response('today.html', today_articles_dic)


def gzh_updated(request):
    gzh_dict = {}
    gzhs = []
    _ids = []
    try:
        gzhs_list = GZH.objects.all()[0:]
    except:
        pass
    for _gzh in gzhs_list:
        gzh_id = _gzh.weixin_id

        for article in Article.objects.filter(gzh__weixin_id__exact=gzh_id):
            print(article.title)
            today = time.strftime('%Y-%m-%d')
            print('today=' + today)
            if article.publish_date == today:
                gzh_updated = article.gzh.weixin_id
                print('update=' + gzh_updated)
                if article.gzh.weixin_id not in _ids:
                    _ids.append(article.gzh.weixin_id)
                    gzhs.append(article)

    paginator = Paginator(gzhs, 30)
    page = request.GET.get('page')
    try:
        _gzhs = paginator.page(page)
    except PageNotAnInteger:
        _gzhs = paginator.page(1)
    except EmptyPage:
        _gzhs = paginator.page(paginator.num_page)

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

    paginator = Paginator(_article, 30)
    page = request.GET.get('page')
    try:
        _article_list = paginator.page(page)
    except PageNotAnInteger:
        _article_list = paginator.page(1)
    except EmptyPage:
        _article_list = paginator.page(paginator.num_page)

    article_updated_dict = {'articles': _article_list}
    return render_to_response('articles_updated.html', article_updated_dict)


def delete_id(request):
    if request.method == 'POST':
        status_dict = {'success': True}
        return HttpResponse(json.dumps(status_dict), content_type='application/json')


def fuzzy_search_spider(request):
    _ids = request.POST.getlist('gzh')
        # print(_ids)
    gzh = Wechat_gzh(_ids)
    gzh.gzh_info_list()

    return index(request)


def cookies_changed(request):
    if request.method=='POST':
        cookies = request.POST.get('cookies')
        print(cookies)
        f = open('cookies.txt', 'w')
        f.write(cookies)
        f.close
        return index(request)
    return render_to_response('cookies_change.html', {})