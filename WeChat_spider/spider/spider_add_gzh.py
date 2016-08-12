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


class Wechat_gzh():
    def __init__(self, key_words):
        self.kws = key_words
        self.host = 'http://weixin.sogou.com/weixin?type=1&query='
        self.gzh_info = []
        self.cookies = {
            'ABTEST': '0|1469412044|v1',
            'SNUID': '893EA94B9294AAFDB77B7FDE926A6AAB',
            'IPLOC': 'CN3700',
            'SUID': '18AC3BDA433E900A00000000579572CC',
            'JSESSIONID': 'aaadvUENQmZQYe-rf6Pxv',
            'SUV': '1469412047751761',
            'weixinIndexVisited': '1',
            'sct': '4',
            'ppinf': '5|1469501867|1470711467|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxMTppJUUyJTgwJTg2b3xjcnQ6MTA6MTQ2OTUwMTg2N3xyZWZuaWNrOjExOmklRTIlODAlODZvfHVzZXJpZDo0NDo4M0JEMzQ5QUE4QUE5MTlBMzFENjUyMUM1Q0IyRDAxRkBxcS5zb2h1LmNvbXw',
            'pprdig': 'lM6Ym9QoLOesylGeaS5w8B7nz2XyVdAEmLf4mTg7EAY61vjFJQi3f_E20yG4UsK0Ifx2yXNE7rjK1wbkQQI9G0LW4d_Q8MKmg0B1KODSLkzJw2_0UQRpIhz0YTBQs6pkBbdVOhOsRAX7VimSh5TXRL8krfsXkysfhg7FzqvOFfQ',
            'ppmdig': '14695018670000008f623b041a9ba269ad4843f719b36d3c',
            'PHPSESSID': '8g0c1nf9v59uluglmgc4dmnk25',
            'SUIR': '893EA94B9294AAFDB77B7FDE926A6AAB',
            'sucessCount': '1|Tue, 26 Jul 2016 03:48:00 GMT',
            'LSTMV': '513 % 2C137',
            'LCLKINT': '33357'
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

        for key_word in self.kws:

                wechat_search_url = self.host + key_word
                # wechat_search_url = self.host + '钓鱼' + '&page=' + str(i)
                print(wechat_search_url)
                # print('page='+str(i))
                try:
                    r = requests.get(wechat_search_url, headers=self.headers, cookies=self.cookies)
                except:
                    pass
                sleep(5)
                # print(r.content)
                soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")
                # print(soup)
                for items in soup.findAll('div', {'class': 'wx-rb'}):
                    # print(items)
                    # print('llllllll')
                    name = items.find('h3').text
                    print('name='+name)
                    wx_id = items.find('label').text
                    print('account='+wx_id)
                    # print(wx_id)
                    fun_infos = items.select('.sp-txt')
                    fun_info = fun_infos[0].text
                    print('introduction='+fun_info)
                    try:
                        wxrz = fun_infos[1].text
                        print('verify_name='+wxrz)
                    except IndexError:
                        pass
                    gzh_paper_url = items.get('href')
                    # print(gzh_paper_url)
                    gzh_head_pics = items.find_all("img")  # 公众号头像

                    gzh_head_pic = gzh_head_pics[0].get('src')
                    path = settings.STATIC_PATH + '/images'

                    os.chdir(path)
                    os.getcwd()
                    f_name = wx_id + '.png'
                    # 保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片
                    conn = urllib.request.urlopen(gzh_head_pic)
                    f = open(f_name, 'wb')
                    f.write(conn.read())
                    f.close()
                    print('Pic Saved!')


                    qr_code = gzh_head_pics[2].get('src')
                    print('gzh_head_pic='+gzh_head_pic)
                    print('qr_code='+qr_code)

                    # try:
                    gzh = add_info(gzh_name=name, id=wx_id, pic=gzh_head_pic, qr_code=qr_code, wxrz=wxrz, info=fun_info)
                    print('add_info ok')
                    # except:
                    #     print('add gzh error')


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
                            print('content_raw error')
                        sleep(5)
                        soup_paper_raw = BeautifulSoup(content_raw.content.decode('utf-8', 'ignore'), "html.parser")
                        # print(soup)
                        date_item = soup_paper_raw.select('#post-date')
                        if len(date_item) != 0:
                            date = date_item[0].text
                            print('date='+date)
                        else:
                            date = []

                        content_item = soup_paper_raw.select('#img-content #js_content')
                        if len(content_item) != 0:
                            content = content_item[0].text
                        else:
                            content = []
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
                            print('add article success')
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


def add_paper(name, title, content, date, source_url=[], video_url=[]):
    paper_list = Article.objects.get_or_create(gzh=name, title=title)[0]
    # paper_list.gzh = name
    paper_list.title = title
    paper_list.content = content
    paper_list.publish_date = date
    paper_list.source_url = source_url
    paper_list.video_url = video_url

    paper_list.save()
    return paper_list


#
# def main():
#     key_words = ['SINA_NBA']
#     wx = Wechat_gzh(key_words)
#     wx.gzh_info_list()
#
#
# if __name__ == '__main__':
#     main()
