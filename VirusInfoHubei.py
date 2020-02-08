# -*- coding: utf-8 -*-

' Virus Info Hubei '

__author__ = 'Jiahui Zhang'

# 2020/2/8完成
# 从湖北卫健委网站-动态要闻（http://wjw.hubei.gov.cn/fbjd/dtyw/）中的“湖北省新型冠状病毒感染的肺炎疫情情况”文本中获取每日疫情信息数据，导出为txt
# 由于卫健委网站无法爬虫，需要将情况信息复制到本地txt文本中
# 并需要将所有的“其中”字样改为“新增确诊病例中”、“新增死亡病例中”、“新增出院病例中”、“确诊病例中”、“死亡病例中”、“出院病例中”
# 如果文本中的城市不是标准格式（没有“市”、“州”字样（神农架林区除外））或一些其他情况，会出现局部bug，建议导出后进行人工核查（分类加和等于总数即可）

import re
import pandas as pd
import numpy as np

# 使用者需要指定以下变量：
inputpath = 'your/path/inputtext.txt'
outputpath = 'your/path/outputtext.txt'

city_list = ['武汉市','孝感市','黄冈市','随州市','荆州市','荆门市','宜昌市','黄石市','襄阳市','鄂州市','仙桃市','十堰市','咸宁市','天门市','潜江市','恩施州','神农架林区']
area_list = ['湖北省'] + city_list

def datap(input,output):
    text = []
    with open(input,'r',encoding='utf-8') as f:
        text = f.read()
    pattern = r',|\.|\n|/|;|：|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    result = re.split(pattern,text)

    while True:
        try:
            result.remove('')
        except:
            break

    title = ['累计确诊','累计疑似','累计重症','累计死亡','累计治愈','累计密接','在院治疗','危重症','已解除医观','尚在医观','发热门诊接诊总数','留观人数','新增确诊','新增疑似','新增重症','新增死亡','新增治愈','新增密接']
    df = pd.DataFrame(np.zeros([18,18]),columns=title,index=area_list)

    def putdata(index,column,val):
        val = int(val)
        try:
            df.loc[index,column] = val
        except:
            print("error,index:",index,"column:",column,"val:",val)

    def provmatch(string,title,text):
        m = re.match(string,text)
        if m:
            putdata('湖北省',title,m.group(1))
            return 1
        return 0

    i = 0
    while i < len(result):
        p = i
        if provmatch(r'.*省.*?新增.*?感染.*?(\d{1,8})例','新增确诊',result[i]):
            i += 1
            continue
        elif provmatch(r'.*新增死亡.*?(\d{1,8})例','新增死亡',result[i]):
            i += 1
            continue
        elif provmatch(r'.*新增出院.*?(\d{1,8})例','新增治愈',result[i]):
            i += 1
            continue
        if '新增确诊病例中' in result[i]:
            i += 1
            while '市' in result[i] or '州' in result[i] or '林区' in result[i]:
                m = re.match(r'((.*?市|.*?州|神农架林区)).*?(\d{1,8})例',result[i])
                if m:
                    putdata(m.group(1),'新增确诊',m.group(3))
                i += 1
        if '新增死亡病例中' in result[i]:
            i += 1
            while '市' in result[i] or '州' in result[i] or '林区' in result[i]:
                m = re.match(r'((.*?市|.*?州|神农架林区)).*?(\d{1,8})例',result[i])
                if m:
                    putdata(m.group(1),'新增死亡',m.group(3))
                i += 1
        if '新增出院病例中' in result[i]:
            i += 1
            while '市' in result[i] or '州' in result[i] or '林区' in result[i]:
                m = re.match(r'((.*?市|.*?州|神农架林区)).*?(\d{1,8})例',result[i])
                if m:
                    putdata(m.group(1),'新增治愈',m.group(3))
                i += 1
        if provmatch(r'.*省.*感染.*?(\d{1,8})例','累计确诊',result[i]) and '新增' not in result[i]:
            i += 1
            continue
        elif provmatch(r'.*死亡.*?(\d{1,8})例','累计死亡',result[i]) and '新增' not in result[i]:
            i += 1
            continue
        elif provmatch(r'.*出院.*?(\d{1,8})例','累计治愈',result[i]) and '新增' not in result[i]:
            i += 1
            continue
        elif provmatch(r'.*重症.*?(\d{1,8})例','累计重症',result[i]) and '新增' not in result[i] and '危' not in result[i]:
            i += 1
            continue
        elif provmatch(r'.*危重症.*?(\d{1,8})例','危重症',result[i]) and '新增' not in result[i]:
            i += 1
            continue
        if '确诊病例中' in result[i]:
            i += 1
            while '市' in result[i] or '州' in result[i] or '林区' in result[i]:
                m = re.match(r'((.*?市|.*?州|神农架林区)).*?(\d{1,8})例',result[i])
                if m:
                    putdata(m.group(1),'累计确诊',m.group(3))
                i += 1
        if '死亡病例中' in result[i]:
            i += 1
            while '市' in result[i] or '州' in result[i] or '林区' in result[i]:
                m = re.match(r'((.*?市|.*?州|神农架林区)).*?(\d{1,8})例',result[i])
                if m:
                    putdata(m.group(1),'累计死亡',m.group(3))
                i += 1
        if '出院病例中' in result[i]:
            i += 1
            while '市' in result[i] or '州' in result[i] or '林区' in result[i]:
                m = re.match(r'((.*?市|.*?州|神农架林区)).*?(\d{1,8})例',result[i])
                if m:
                    putdata(m.group(1),'累计治愈',m.group(3))
                i += 1
        if provmatch(r'.*密切接触.*?(\d{1,8})人','累计密接',result[i]):
            i += 1
            continue
        elif provmatch(r'.*解除医学观察.*?(\d{1,8})人','已解除医观',result[i]):
            i += 1
            continue
        elif provmatch(r'.*?(\d{1,8})人正在接受医学观察','尚在医观',result[i]):
            i += 1
            continue
        elif provmatch(r'.*?接受医学观察(\d{1,8})人','尚在医观',result[i]):
            i += 1
            continue
        if provmatch(r'.*?发热门诊.*?(\d{1,8})人','发热门诊接诊总数',result[i]):
            i += 1
            if provmatch(r'留观(\d{1,8}).*?','留观人数',result[i]):
                i += 1
            while '市' in result[i] or '州' in result[i] or '林区' in result[i]:
                m = re.match(r'(.*?市|.*?州|神农架林区)(\d{1,8}).*?',result[i])
                city = m.group(1)
                putdata(city,'发热门诊接诊总数',m.group(3))
                i += 1
                m = re.match(r'留观(\d{1,8}).*?',result[i])
                if m:
                    putdata(city,'留观人数',m.group(1))
                else:
                    putdata(city,'留观人数',0)
                i += 1
        if i == p:
            i += 1
        # print(i,'/',len(result))

    print(df)
    df.to_csv(output, sep=',', header=True, index=True,encoding='utf-8')

if __name__ == "__main__":
    datap(inputpath,outputpath)