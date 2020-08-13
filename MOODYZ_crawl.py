# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

url = 'https://www.moodyz.com/works/list/new_reserve/'
res = requests.get(url)

##番号和图片地址确定
work_num = []
src = []
title = []
html = BeautifulSoup(res.text, features="lxml")
for link in html.find_all('img'):
    src.append(link.get('src'))
del src[0]
for name in html.find_all('img'):
    title.append(name.get('alt'))
del title[0]
for str in src:
    wn1 = str.split('/')[-1]
    wn2 = wn1.split('-')[0]
    work_num.append(wn2)

# #图片下载
# for src1 in src:
#     src1 = 'https://www.moodyz.com' + src1
#     time.sleep(0.1)
#     r = requests.get(src1)
#     picture_name = src1.split('/')[-1]
#     with open('20200813/' + picture_name, "wb")as f:
#         f.write(r.content)

##内容提取
introduces = []
actress_name = []
date = []
duration = []
for wn in work_num:
    url = 'https://www.moodyz.com/works/detail/' + wn
    res_wn = requests.get(url)
    html_wn = BeautifulSoup(res_wn.text, features="lxml")
    introduces.append(html_wn.find('div', {'works-detail-desc-tx'}).text.replace("\n", ""))
    name_bridge = html_wn.find('ul', {'works-detail-info--actress'})
    if name_bridge is None:
        actress_name.append(None)
    else:
        name_bridge_2 = name_bridge.find('li', {'js-toggle-target--actress'}).text.replace("\n", "")
        actress_name.append(name_bridge_2[4:])
    date_bridge = html_wn.find('ul', {'works-detail-info'})
    date.append(date_bridge.find(string=re.compile("2020")))
    duration_bridge = html_wn.find_all('div', {'works-detail-inner'})
    duration_bridge_2 = duration_bridge[1].find_all('li')
    duration.append(duration_bridge_2[4].text.replace("\n", ""))


# url = 'https://www.moodyz.com/works/detail/miaa304/'
# res_wn = requests.get(url)
# html_wn = BeautifulSoup(res_wn.text, features="lxml")
# introduces.append(html_wn.find('div', {'works-detail-desc-tx'}).text.replace("\n", ""))
# name_bridge = html_wn.find('ul', {'works-detail-info--actress'})
# if name_bridge is None:
#     actress_name.append(None)
# else:
#     name_bridge_2 = name_bridge.find('li', {'js-toggle-target--actress'}).text.replace("\n", "")
#     actress_name.append(name_bridge_2[4:])
# date_bridge = html_wn.find('ul', {'works-detail-info'})
# date.append(date_bridge.find(string=re.compile("2020")))
# duration_bridge = html_wn.find_all('div', {'works-detail-inner'})
# duration_bridge_2 = duration_bridge[1].find_all('li')
# duration.append(duration_bridge_2[4].text)
#
# print(name_bridge)




##保存到CSV文件
list = [work_num, title]
data = {
    '番号': work_num,
    '影片名': title,
    '女优姓名': actress_name,
    '详情': introduces,
    '发售日期': date,
    '时长': duration
}
df = pd.DataFrame(data)
df.to_csv("C:/Users/RHB/Desktop/graduated/coding/MOODYZ_crawl/20200813/data.csv", encoding='utf_8_sig')
