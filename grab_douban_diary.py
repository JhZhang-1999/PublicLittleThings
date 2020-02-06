# -*- coding: utf-8 -*-

' Grab Douban Diary '

__author__ = 'Jiahui Zhang'

# 2020/2/5完成的豆瓣日记爬虫，输入豆瓣id爬取该id对应用户所有豆瓣日记，按时间-标题的格式存储；无需登录豆瓣

import requests
import lxml
import re
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

# 使用者需设定以下两个变量：
outputpath = 'D:/your/local/path/'
dbid = 'your_douban_id'

def index_pages(number):
    url = 'https://www.douban.com/people/%s/notes?start=%d&type=note' % (dbid, number)
    index_response = requests.get(url=url,headers=headers)
    tree = etree.HTML(index_response.text)
    m_urls = tree.xpath("//div[@class='note-header-container']/h3/a/@href")
    return m_urls

def get_contents(url):
    index_response = requests.get(url=url,headers=headers)
    tree = etree.HTML(index_response.text)
    title = tree.xpath("//div[@class='note-header note-header-container']/h1/text()")
    title = title[0]
    content = tree.xpath("//div[@class='note']//text()")
    time = tree.xpath("//div/span[@class='pub-date']/text()")
    time = time[0]
    author = tree.xpath("//div[@class='note-header note-header-container']/div/a/text()")
    author = author[0]
    pathstr = outputpath + time.replace(':','-') + title.replace('|','') + '.txt'
    with open(pathstr, 'w', encoding='utf-8') as f:
        f.write(title+"\n")
        f.write(time+'\n')
        f.write('author: ' + author + '\n')
        f.write('url: ' + url + '\n')
        f.write('\n')
        for lines in content:
            f.write(lines + '\n')
    print("Finished writing " + title)

if __name__ == '__main__':
    i = 0
    while True:
        urls = index_pages(i)
        if len(urls) == 0:
            break
        for url in urls:
            get_contents(url)
        i += 10
