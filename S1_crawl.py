import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

url = 'https://www.s1s1s1.com/works/list/reserve/'
res = requests.get(url)
work_num = []
src = []
src_p = []
title = []

# 内容提取
html = BeautifulSoup(res.text, features="lxml")
main_content = html.find('div', {'class': 'main-content'})
reserve_list = main_content.find('section', {'class': 'p-works-list-reserve'})
work_list = reserve_list.find('ul', {'class': 'c-works-list'})
work_list_item = work_list.find_all('li', {'class': 'c-works-list-item'})

# 番号与图片地址的确定
for link in html.find_all('img'):
    src.append('https://www.s1s1s1.com' + link.get('src'))
    src_p.append(link.get('src'))
del src[0]
del src_p[0]
for name in work_list.find_all('img'):
    title.append(name.get('alt'))
for str in src_p:
    work_num.append(str[16:23])

#封面下载
for src1 in src:
    time.sleep(0.1)
    r = requests.get(src1)
    picture_name = src1.split('/')[-1]
    with open('20200907/' + picture_name, "wb")as f:
        f.write(r.content)

##详细内容##
introduces = []
actress_name = []
date = []
duration = []
for wn in work_num:
    url = 'https://www.s1s1s1.com/works/detail/' + wn
    res_wn = requests.get(url)
    html_wn = BeautifulSoup(res_wn.text, features="lxml")
    introduce = html_wn.find('p', {'works-detail-tx'}).text
    introduces.append(introduce)
    name_bridge = html_wn.find('li', {'works-detail-info-item js-toggle-target--actress'})
    # name_bridge_1 = name_bridge.find('a')
    name_clean = name_bridge.text.replace("\n", "")
    name_clean_2 = name_clean[2:]
    actress_name.append(name_clean_2)
    date_bridge = html_wn.find('ul', {'works-detail-info-lst'})
    date_bridge_2 = date_bridge.find(string=re.compile("2020"))
    date.append(date_bridge_2)
    duration_bridge = html_wn.find_all('li', {'works-detail-info-desc-txt-item works-detail-info-desc-txt-item--stream works-detail-info-desc-txt-item--fix'})
    duration.append(duration_bridge[1].text)


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
df = df.loc[df['发售日期'] == '2020年9月7日']
df.to_csv("C:/Users/RHB/Desktop/graduated/coding/S1_crawl/20200907/data.csv", encoding='utf_8_sig')


#####施工中######
# class S1(object):
#
#     def __init__(self, work_num):
#         self.work_num = work_num
#
#     def get_work_num(self):
#         work_num = []
#         src = []
#         src_p = []
#         title = []
#         for link in html.find_all('img'):
#             src.append('https://www.s1s1s1.com/' + link.get('src'))
#             src_p.append(link.get('src'))
#         del src[0]
#         del src_p[0]
#         for name in work_list.find_all('img'):
#             title.append(name.get('alt'))
#         for str in src_p:
#             work_num.append(str[16:23])
#         return work_num
#
#     def work_cover(self, work_num):
#         time.sleep(0.1)
#         src1 = 'https://www.s1s1s1.com/contents/works/' + work_num + '/' + work_num + '-ps.jpg'
#         r = requests.get(src1)
#         picture_name = src1.split('/')[-1]
#         with open('731-819/' + picture_name, "wb")as f:
#             f.write(r.content)
