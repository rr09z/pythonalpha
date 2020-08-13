import requests
import json
import datetime
from bs4 import BeautifulSoup
import pandas as pd


# url = 'http://hq.sinajs.cn/list=fx_susdcnh'
# res = requests.get(url)
# print(res.text)

today = str(datetime.date.today())


def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday


yesterday = str(getYesterday())
print(yesterday)
print(today)
url = 'http://market.finance.sina.com.cn/pricehis.php?symbol='+'sh600900'+'&startdate=' + yesterday + '&enddate=' + today
res = requests.get(url)
html = BeautifulSoup(res.text, features='lxml')
# print(html.text)
data = html.find('tbody')
data1 = data.find_all('td')
transaction_price = []
transaction_volume = []
percentage = []
try:
    for n in range(0, 300):
        if n % 3 == 0:
            transaction_price.append(data1[n].text)
        elif n % 3 == 1:
            transaction_volume.append(data1[n].text)
        else:
            percentage.append(data1[n].text)
        n = n + 1
except IndexError:
    print('list index out of range')
Data = {'成交价': transaction_price,
        '成交量': transaction_volume,
        '占比': percentage
        }
df = pd.DataFrame(Data)
# print(data1[200].text)