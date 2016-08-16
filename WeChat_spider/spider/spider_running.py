#!/bin/env /usr/local/bin/python3
# coding: utf-8
import requests, re, urllib.request
from bs4 import BeautifulSoup
from time import sleep
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeChat_spider.settings')

import django

django.setup()

from wechat_gzh.models import GZH, Article


class WXGZH():
    def __init__(self, gzh_id):
        self.gzh_id = gzh_id
        self.host = 'http://weixin.sogou.com/weixin?type=1&query='
        self.gzh_info = []
        self.cookies = {

        }
        self.headers = {
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep - alive',
            'Host': 'weixin.sogou.com',
            'Referer': 'http://weixin.sogou.com/weixin?query=%E9%92%93%E9%B1%BC&_sug_type_=&sut=2960&lkt=2,1469418101779,1469418103662&_sug_=y&type=1&sst0=1469418103770&page=1&ie=utf8&w=01019900&dr=1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
        }

    def gzh_info_list(self):
        cookies_raw = open('../cookies.txt').read()
        _cookies_raw = cookies_raw.replace('\r', '').replace('\n', '').split(';')

        for _cookies in _cookies_raw:
            coolies = _cookies.split('=')
            self.cookies[coolies[0]] = coolies[1]

        wechat_search_url = self.host + self.gzh_id
        print(wechat_search_url)
        try:
            r = requests.get(wechat_search_url, headers=self.headers, cookies=self.cookies)
        except ConnectionError:
            pass
        sleep(4)
        # print(r.content)
        soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")
        # print(soup)
        for items in soup.findAll('div', {'class': 'wx-rb'}):
            gzh_paper_url = items.get('href')
            name = items.find('h3').text

            try:
                gzh = add_info(gzh_name=name)
                print('add info ok')
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
                r = requests.get(url=gzh_paper_url, headers=paper_headers, timeout=2)
                print('gzh_paper_url ok ')
            except:
                print('解析paper_url 错误')
            sleep(5)
            html = r.content.decode('utf-8', 'ignore')
            # print(r.content.decode('utf-8', 'ignore'))
            # print(type(html))

            paper_titles_raw = re.findall(r'title(.*?)digest', html)
            paper_urls_raw = re.findall(r'content_url(.*?)source_url', html)

            for i in range(len(paper_titles_raw)):
                paper_title = replace_html(str(paper_titles_raw[i]))
                paper_url_raw = replace_html(str(paper_urls_raw[i]))
                paper.append(paper_title)
                if paper != '':
                    change = True

                ############文章链接、题目
                paper_url = "http://mp.weixin.qq.com" + paper_url_raw
                print('paper_url=' + paper_url)
                print('paper_title=' + paper_title)
                ##############文章内容、日期、原文链接
                try:
                    content_raw = requests.get(url=paper_url, headers=paper_content_headers,
                                               cookies=paper_content_cookies, timeout=2)

                except requests.exceptions.ConnectionError:
                    r.status_code = "Connection refused"
                sleep(5)
                soup_paper_raw = BeautifulSoup(content_raw.content.decode('utf-8', 'ignore'), "html.parser")
                # print(soup)
                date_item = soup_paper_raw.select('#post-date')
                if len(date_item) != 0:
                    date = date_item[0].text
                    print('date=' + date)
                else:
                    date = ''

                content_item = soup_paper_raw.select('#img-content #js_content')
                if len(content_item) != 0:
                    content = content_item[0].text
                else:
                    content = ''

                paper_html = content_raw.content.decode('utf-8', 'ignore')

                source_url_raw = re.findall(r'msg_source_url = \'(.*?)\';', paper_html)
                if len(source_url_raw) != 0:
                    source_url = replace_html(str(source_url_raw[0]))
                    print('source_url=' + source_url)
                else:
                    source_url = ''

                try:
                    iframe = soup_paper_raw.iframe
                    video_url_raw = iframe.get('data-src')
                    video_url = replace_html(str(video_url_raw))
                    print('video_url=' + video_url)
                except:
                    video_url = ''
                print('before')
                try:
                    add_paper(name=gzh, title=paper_title, content=content, date=date, source_url=source_url,
                              video_url=video_url, change=change)
                    print('add article')
                except:
                    print('add paper error')

                            ##########################################


def add_info(gzh_name='', id='', pic='', qr_code='', wxrz='', info=''):
    g_i = GZH.objects.get_or_create(name=gzh_name)[0]
    print(g_i)
    print('ok')
    g_i.save()
    return g_i


def add_paper(name, title, content, date, source_url, video_url, change):
    paper_list = Article.objects.get_or_create(gzh=name, title=title)[0]
    # paper_list.gzh = name
    paper_list.title = title
    paper_list.content = content
    paper_list.publish_date = date
    paper_list.source_url = source_url
    paper_list.video_url = video_url
    paper_list.change = change
    paper_list.save()

    return paper_list


def main():
    gzh_list = GZH.objects.all()
    for gzh in gzh_list:
        gzh_id = gzh.weixin_id
        _gzh = WXGZH(gzh_id)
        _gzh.gzh_info_list()


if __name__ == '__main__':
    main()





