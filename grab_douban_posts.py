# -*- coding: utf-8 -*-

' Grab Douban Posts '

__author__ = 'Jiahui Zhang'

# 2020/2/6完成的豆瓣广播爬虫，爬取指定用户的所有广播，一页存储一个txt文件；需使用用户名密码模拟登录豆瓣
# 参考教程：https://blog.csdn.net/haeasringnar/article/details/82558729
# 支持的广播类型：普通动态（可带图）、转发动态（提取转发文字和原动态url）、书影音游动态（提取评价文字和书影音游信息url）

import requests
import lxml
import re
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

# 使用者需指定以下变量
NAME = 'name' # 豆瓣登录名
PASSWORD = 'password' # 豆瓣登录密码
DBID = 'douban_id' # 要查看广播的用户id
PATHSTORE = 'D:/store/' # 存放页面的地址
PATHOUTPUT = 'D:/output/' # 存放导出动态的地址
MAXPAGE = 30 # 从第1页至第30页的动态

def get_contents_to_local():
    s = requests.session()
    url_basic = 'https://accounts.douban.com/j/mobile/login/basic'
    data = {
        'ck': '',
        'name': NAME,
        'password': PASSWORD,
        'remember': 'false',
        'ticket': ''
    }
    r = s.post(url=url_basic, data=data, headers=headers)
    for i in range(1,MAXPAGE+1,1):
        url = 'https://www.douban.com/people/%s/statuses?p=%d' % (DBID, i)    
        index_response = s.get(url=url, headers=headers)
        with open(PATHSTORE + str(i) + '.txt','w',encoding='utf-8') as f:
            f.write(index_response.text)
        print("Wrote page %d successfully" % i)

def get_contents_from_local(path,page):
    with open(path,'r',encoding='utf-8') as f:
        text = f.read()
    tree = etree.HTML(text)
    i = 1
    while True:
        try:
            dclass = tree.xpath("//div[@class='stream-items']/div[%d]/@class" % i)[0]
        except:
            print("Finished page%d" % page)
            break
        if dclass == 'new-status status-wrapper    ': # 书影音游
            with open(PATHOUTPUT + str(page) + '.txt','a',encoding='utf-8') as f:
                try:
                    time = tree.xpath("//div[@class='stream-items']/div[%d]/div/div/div/div/span/a/text()" % i)[0]
                    f.write('Time: '+str(time)+'\n')
                except:
                    f.write('Time: not applicable\n')
                try:
                    info = tree.xpath("//div[@class='stream-items']/div[%d]/div/div/div/div/div/div/a/text()" % i)[0]
                    f.write('About: '+str(info)+'\n')
                except:
                    f.write("About: not applicable\n")
                try:
                    infos = tree.xpath("//div[@class='stream-items']/div[%d]/div/div/div/div/div/div/a/@href" % i)[0]
                    f.write("About\'s url: "+str(infos)+'\n')
                except:
                    pass
                try:
                    text = tree.xpath("//div[@class='stream-items']/div[%d]/div/div/div/div/blockquote/p/text()" % i)[0]
                    f.write('Text: \n'+str(text)+'\n')
                except:
                    f.write('Text: not applicable\n')
                f.write('\n')
        elif dclass == 'new-status status-wrapper    saying': # 纯动态
            with open(PATHOUTPUT + str(page) + '.txt','a',encoding='utf-8') as f:
                try:
                    time = tree.xpath("//div[@class='stream-items']/div[%d]/div/div/div/div/span/a/text()" % i)[0]
                    f.write('Time: '+str(time)+'\n')
                except:
                    f.write('Time: not applicable\n')
                try:
                    pic = tree.xpath("//div[@class='stream-items']/div[%d]/div/div/div/div/div/div/span/img/@src" % i)[0]
                    f.write('Picture url: '+str(pic)+'\n')
                except:
                    pass
                try:
                    text = tree.xpath("//div[@class='stream-items']/div[%d]/div/div/div/div/blockquote/p/text()" % i)[0]
                    f.write('Text: \n'+str(text)+'\n')
                except:
                    f.write('Text: not applicable\n')
                f.write('\n')
        elif dclass == 'new-status status-wrapper status-reshared-wrapper   saying': # 转发动态
            with open(PATHOUTPUT + str(page) + '.txt','a',encoding='utf-8') as f:
                try:
                    time = tree.xpath("//div[@class='stream-items']/div[%d]/div/div/div/div/span/a/text()" % i)[0]
                    f.write('Time: '+str(time)+'\n')
                except:
                    f.write('Time: not applicable\n')
                try:
                    source = tree.xpath("//div[@class='stream-items']/div[%d]/div/@data-status-url" % i)[0]
                    f.write('Reshare source url: '+str(source)+'\n')
                except:
                    pass
                try:
                    text = tree.xpath("//div[@class='stream-items']/div[%d]/div/div/div/div/blockquote/text()" % i)[0]
                    f.write('Text: \n'+str(text)+'\n')
                except:
                    f.write('Text: not applicable\n')
                f.write('\n')
        i += 1

if __name__ == '__main__':
    get_contents_to_local()
    for p in range(1,MAXPAGE+1,1):
        path = PATHSTORE + str(p) + '.txt'
        get_contents_from_local(path,p)
