from django.shortcuts import render, render_to_response, RequestContext
from wechat_gzh.models import GZH, Article
from wechat_gzh.forms import GZHForm
from wechat_gzh.add_gzh import WXGZH
from django.template import RequestContext
import time


def index(request):
    gzh_list = GZH.objects.all()
    gzh_dict = {'gzhs': gzh_list}

    return render_to_response('index.html', gzh_dict)


def article(request, gzh_id):
    article_list = Article.objects.filter(gzh__weixin_id__exact=gzh_id)
    # print('list')
    article_dict = {'articles': article_list}

    return render_to_response('article_list.html', article_dict)


def article_content(request, id):
    # content_dict = {}
    article = Article.objects.filter(id=id)[:1]
    content_dict = {'contents': article}

    return render_to_response('article_content.html', content_dict)


def add_gzh(request):
    print('ok1')
    if request.method == 'POST':
        print('ok2')
        form = GZHForm(request.POST)
        # print(dir(form))
        if form.is_valid():
            print(form.cleaned_data['weixin_id'])
            print('ok3')
            # form.save()
            id = form.cleaned_data['weixin_id']
            gzh = WXGZH(id)
            gzh.gzh_info_list()
            print('ok4')
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
        for i in range(10):
            article_list = Article.objects.filter(gzh__weixin_id__exact=gzh_id)[i]
            today = time.strftime('%Y-%m-%d')

            if article_list.publish_date == today:
                new_article.append(article_list)
                today_articles_dic = {'new_articles': new_article}
    except:
        pass
    return render_to_response('today.html', today_articles_dic)


