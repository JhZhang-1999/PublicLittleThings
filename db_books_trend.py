# --*-- coding: utf-8 --*--

' Grab Douban Diary '

__author__ = 'Jiahui Zhang'

# 2020/2/9完成的豆瓣新书数据动态追踪；定期运行该文件可以建立对于每本新书的一个txt数据表，可供分析使用

import requests
import lxml
import re
from lxml import etree
import pandas as pd
import time

# 使用者需指定以下变量，为一个存放数据的文件夹，并在文件夹中建立名为"booklist.txt"的空文件
MYPATH = 'your/path/'

def get_date():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
url_basic = 'https://book.douban.com/latest?icn=index-latestbook-all'
initializer = ['score','people','5','4','3','2','1']

def get_latest_books():
    index_response = requests.get(url=url_basic,headers=headers)
    tree = etree.HTML(index_response.text)
    book_url = tree.xpath("//div[@class='grid-12-12 clearfix']/div/ul/li/a/@href")
    book_name = tree.xpath("//div[@class='grid-12-12 clearfix']/div/ul/li/div/h2/a/text()")
    for i in range(len(book_name)):
        book_name[i] = book_name[i].replace(':','：').replace('?','？')
    return zip(book_name,book_url)

def write_txt(df,bookname,init=False):
    path = MYPATH + str(bookname) + '.txt'
    with open(path,'a',encoding = 'utf-8') as f:
        if init == True:
            for i in range(df.shape[1]):
                f.write(',' + initializer[i])
            f.write('\n')
        index = df.shape[0]
        f.write(str(df.index.values[index-1]))
        for i in range(df.shape[1]):
            f.write(',' + str(df.iloc[index-1,i]))
        f.write('\n')
    return

def get_book_info(url,bookname,init=False):
    date = get_date()
    if init == True:
        df = pd.DataFrame()
        for obj in initializer:
            df.loc[date,obj] = 0
    else:
        path = MYPATH + str(bookname) + '.txt'
        df = pd.read_csv(path,header=0,index_col=[0])
        if df.index.values[-1] == date:
            return
    index_response = requests.get(url=url,headers=headers)
    tree = etree.HTML(index_response.text)
    total_score = tree.xpath("//div[@class='rating_self clearfix']/strong/text()")[0]
    df.loc[date,'score'] = total_score
    try:
        total_people = int(tree.xpath("//div[@class='rating_sum']/span/a/span/text()")[0])
        df.loc[date,'people'] = total_people
        stars = tree.xpath("//div[@class='rating_wrap clearbox']/span/text()")
        for obj,st in zip(initializer[2:],range(1,10,2)):
            df.loc[date,obj] = round(float(stars[st][:-1])/100*total_people)
    except:
        total_people = 0
    write_txt(df,bookname,init)

if __name__ == '__main__':
    # 首先追踪已在booklist上的书
    path = MYPATH + 'booklist.txt'
    booklist = []
    urllist = []
    with open(path,'r',encoding='utf-8') as f:
        for line in f:
            t = str(line).replace('\n','').split(',')
            booklist.append(t[0])
            urllist.append(t[1])
    for book,url in zip(booklist,urllist):
        get_book_info(url,book,0)

    # 获取当前新书速递中的书
    zippack = get_latest_books()
    for pack in zippack:
        initstate = 1
        if pack[0] in booklist:
            initstate = 0
        get_book_info(pack[1],pack[0],initstate)
        if initstate == 1:
            with open(path,'a',encoding='utf-8') as f:
                f.write(pack[0]+','+pack[1]+'\n')
