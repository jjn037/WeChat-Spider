#!/bin/env /usr/local/bin/python3
# coding: utf-8
import requests, re, urllib.request
from bs4 import BeautifulSoup
from time import sleep
import os, random, sys
from django.conf import settings
import http.cookiejar, urllib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeChat_spider.settings')

import django

django.setup()

from wechat_gzh.models import GZH, Article


class Wechat_gzh():
    def __init__(self, key_words):
        self.kws = key_words
        self.host = 'http://weixin.sogou.com/weixin?type=1&query='
        self.gzh_info = []
        # self.cookies = {
        #     'ABTEST': '7|1471075813|v1',
        #     'SNUID': '58ED7B9A414578AFC8E3405E41DC4A58',
        #     'IPLOC': 'CN3700',
        #     'SUID': '18AC3BDA6A20900A0000000057AED5E5',
        #     'JSESSIONID': 'aaa8-oF-pfer8gRqhiQxv',
        #     'SUV': '00395A07DA3BAC1857AED5E534BB9700',
        #     'weixinIndexVisited': '1',
        #     'sct': '5',
        #     'jrtt_at': 'b6fe2bd0a9337f6ea9420fd12187f960',
        #
        # }
        self.cookies = {}
        self.headers = {
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep - alive',
            'Host': 'weixin.sogou.com',
            'Referer': 'http://weixin.sogou.com/weixin?query=%E9%92%93%E9%B1%BC&_sug_type_=&sut=2960&lkt=2,1469418101779,1469418103662&_sug_=y&type=1&sst0=1469418103770&page=1&ie=utf8&w=01019900&dr=1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
        }
        self.proxy_list = [
            # '112.16.11.129:2226',
            '183.61.236.54:3128',
            '222.161.209.164:8102',

        ]

    def gzh_info_list(self):
        with open('../cookies.txt') as f:
            cookies_raw = f.read()
            _cookies_raw = cookies_raw.replace('\r', '').replace('\n', '').split(';')

            for _cookies in _cookies_raw:
                coolies = _cookies.strip().split('=')
                self.cookies[coolies[0]] = coolies[1]
        # print(self.cookies)

        for key_word in self.kws:
            for i in range(1, 20):  # 此处调试完修改
                # _proxy = random.choice(self.proxy_list)
                # print(_proxy)
                # proxies = {'http': _proxy}
                wechat_search_url = self.host + key_word + '&page=' + str(i)
                # wechat_search_url = self.host + '钓鱼' + '&page=' + str(i)
                print(wechat_search_url)
                print('page='+str(i))
                if i < 10:
                    try:
                        r = requests.get(wechat_search_url, headers=self.headers, timeout=5)
                    except:
                        info = sys.exc_info()
                        print(info[0], ":", info[1])
                        print('get wechat_search_url error')
                else:
                    try:
                        r = requests.get(wechat_search_url, headers=self.headers, cookies=self.cookies, timeout=5)
                    except:

                        print('Timeout occurred')
                    # print(r.content.decode('utf-8', 'ignore'))
                sleep(10)
                # print(r.r.content.decode('utf-8', 'ignore'))
                soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")
                # print(soup)
                for items in soup.findAll('div', {'class': 'wx-rb'}):
                    # print(items)
                    name = items.find('h3').text
                    print('name='+name)
                    wx_id = items.find('label').text
                    if wx_id=='':
                        wx_id = name
                    print('account='+wx_id)
                    print(wx_id)
                    fun_infos = items.select('.sp-txt')
                    fun_info = fun_infos[0].text
                    print('introduction='+fun_info)
                    try:
                        wxrz = fun_infos[1].text
                        print('verify_name='+wxrz)
                    except IndexError:
                        pass
                    gzh_paper_url = items.get('href')
                    print(gzh_paper_url)
                    gzh_head_pics = items.find_all("img")  # 公众号头像

                    gzh_head_pic = gzh_head_pics[0].get('src')
                    path = settings.STATIC_PATH + '/images'

                    os.chdir(path)
                    os.getcwd()
                    f_name = wx_id + '.png'
                    # 保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片
                    try:
                      conn = urllib.request.urlopen(gzh_head_pic)
                    except:
                        pass
                    f = open(f_name, 'wb')
                    f.write(conn.read())
                    f.close()
                    print('Pic Saved!')

                    qr_code = gzh_head_pics[2].get('src')
                    print('gzh_head_pic='+gzh_head_pic)
                    print('qr_code='+qr_code)

                    try:
                        gzh = add_info(gzh_name=name, id=wx_id, pic=gzh_head_pic, qr_code=qr_code, wxrz=wxrz, info=fun_info)
                    except:
                        print('add info error')


                    ########################################公众号文章名字和url抓取
                    paper_content_headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Connection': 'keep-alive',
                        # 'Upgrade-Insecure-Requests' : '1',
                        'Host': 'mp.weixin.qq.com',
                        'Referer': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1469719174&ver=1&signature=cVUmDPWKg3xdcidBjO*ahZUwZYxCl8DbLLg*ZHN6GjNQm8Lydd8LKUzKHqZmJ3*e3K*f8i2odPMFb*njwN2t*g==',
                        # 'Referer' : 'http://weixin.sogou.com/weixin?type=1&query=%E9%92%93%E9%B1%BC',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
                    }
                    paper_content_cookies = {
                        'pgv_pvi': '9305632768',
                        'pgv_si': 's4923546624'
                    }

                    def replace_html(s):
                        s = s.replace('&quot;:', '')
                        s = s.replace('&quot;,', '')
                        s = s.replace('&quot;', '')
                        s = s.replace('&amp;', '&')
                        s = s.replace('amp;', '')
                        s = s.replace('&lt;', '<')
                        s = s.replace('&gt;', '>')
                        s = s.replace('&nbsp;', ' ')
                        s = s.replace(r"\\", r'')
                        return s

                    paper = []
                    paper_headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, sdch',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'Connection': 'keep-alive',
                        # 'Upgrade-Insecure-Requests' : '1',
                        'Host': 'mp.weixin.qq.com',
                        'Referer': 'http://weixin.sogou.com/weixin?type=1&query=%E9%92%93%E9%B1%BC&ie=utf8&_sug_=y&_sug_type_=',
                        # 'Referer' : 'http://weixin.sogou.com/weixin?type=1&query=%E9%92%93%E9%B1%BC',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
                    }

                    try:
                        r = requests.get(url=gzh_paper_url, headers=paper_headers)
                        print(r)
                    except:
                        pass
                    sleep(5)
                    html = r.content.decode('utf-8', 'ignore')
                    # print(r.content.decode('utf-8', 'ignore'))
                    # print(type(html))

                    paper_titles_raw = re.findall(r'title(.*?)digest', html)
                    paper_urls_raw = re.findall(r'content_url(.*?)source_url', html)
                    # print(type(paper_titles_raw))
                    # print(len(paper_url))
                    for i in range(len(paper_titles_raw)):
                        paper_title = replace_html(str(paper_titles_raw[i]))
                        paper_url_raw = replace_html(str(paper_urls_raw[i]))
                        # p = [paper_title, paper_url]
                        # paper.append(p)
                            ############文章链接、题目
                        paper_url = "http://mp.weixin.qq.com" + paper_url_raw
                        print('paper_url='+paper_url)
                        print('paper_title='+paper_title)
                            ##############文章内容、日期、原文链接
                        try:
                            content_raw = requests.get(url=paper_url, headers=paper_content_headers, cookies=paper_content_cookies)

                        except requests.exceptions.ConnectionError:
                            r.status_code = "Connection refused"
                        sleep(5)
                        soup_paper_raw = BeautifulSoup(content_raw.content.decode('utf-8', 'ignore'), "html.parser")
                        # print(soup)
                        date_item = soup_paper_raw.select('#post-date')
                        if len(date_item) != 0:
                            date = date_item[0].text
                            print('date='+date)
                        else:
                            date = ''

                        content_item = soup_paper_raw.select('#img-content #js_content')
                        if len(content_item) != 0:
                            content = content_item[0].text
                        else:
                            content = ''
                        # print(content)
                        #
                        # content_img_url = soup_paper_raw.find_all('#img-content #js_content img')
                        # print(content_img_url)
                        paper_html = content_raw.content.decode('utf-8', 'ignore')
                        # srcs_raw = re.findall(r'data-src=(.*?)data-ratio', paper_html)
                        # # print((srcs_raw))
                        # srcs = replace_html(str(srcs_raw))
                        # print(srcs)
                        source_url_raw = re.findall(r'msg_source_url = \'(.*?)\';', paper_html)
                        if len(source_url_raw) != 0:
                            source_url = replace_html(str(source_url_raw[0]))
                            print('source_url=' + source_url)
                        else:
                            source_url = []

                        try:

                            iframe = soup_paper_raw.iframe
                            video_url_raw = iframe.get('data-src')
                            video_url = replace_html(str(video_url_raw))
                            print('video_url=' + video_url)
                        except:
                            video_url = []


                        try:
                            add_paper(name=gzh, title=paper_title, content=content, date=date, source_url=source_url, video_url=video_url)
                            print('add article')
                        except:
                           print('add paper error')


                        ##########################################

def add_info(gzh_name, id, pic, qr_code, wxrz, info):

    g_i = GZH.objects.get_or_create(name=gzh_name)[0]
    print(g_i)
    print('ok')
    g_i.weixin_id = id
    g_i.head_pic = pic
    g_i.qr_code = qr_code
    g_i.introduction = info
    g_i.verify_name = wxrz
    g_i.save()
    return g_i


def add_paper(name, title, content, date, source_url='', video_url=''):
    paper_list = Article.objects.get_or_create(gzh=name, title=title)[0]
    # paper_list.gzh = name
    paper_list.title = title
    paper_list.content = content
    paper_list.publish_date = date
    paper_list.source_url = source_url
    paper_list.video_url = video_url

    paper_list.save()
    return paper_list


def main():
    key_words = ['钓鱼', '鱼竿', '鱼饵', '钓场', '钓箱', '钓竿', '饵料', '垂钓']
    # key_words = ['钓竿', '饵料']
    wx = Wechat_gzh(key_words)
    wx.gzh_info_list()


if __name__ == '__main__':
    main()
