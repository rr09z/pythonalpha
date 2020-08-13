import requests
import _json
import pandas as pd

stock_num = ['sh600000', 'sh600016', 'sh600019', 'sh600028', 'sh600029', 'sh600030', 'sh600031', 'sh600036', 'sh600048',
             'sh600050', 'sh600104', 'sh600196', 'sh600276', 'sh600309', 'sh600340', 'sh600519', 'sh600585', 'sh600690',
             'sh600703', 'sh600837', 'sh600887', 'sh601066', 'sh601088', 'sh601111', 'sh601138', 'sh601166', 'sh601186',
             'sh601211', 'sh601229', 'sh601288', 'sh601318', 'sh601319', 'sh601328', 'sh601336', 'sh601390', 'sh601398',
             'sh601601', 'sh601628', 'sh601668', 'sh601688', 'sh601766', 'sh601800', 'sh601818', 'sh601857', 'sh601888',
             'sh601939', 'sh601988', 'sh601989', 'sh603259', 'sh603993'
             ]


def stock_crawl(num):
    number = num
    res = requests.get(
        'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=' + number + '&scale=5&ma=5&datalen=48').json()
    df = pd.DataFrame()
    n = 0
    range1 = list(range(0, 48, 1))
    dfsz000001 = pd.DataFrame()
    for n in range1:
        a = res[n]
        for item in a.items():
            list1 = [a]
        # print(list1)
        df = pd.DataFrame(list1)
        # print(df)
        dfsz000001 = pd.concat([dfsz000001, df], axis=0)
        n = n + 1
    return dfsz000001


m = pd.DataFrame()
for num in stock_num:
    n = stock_crawl(num=num)
    n['index'] = num
    m = pd.concat([m, n], axis=0)


data = m.loc[m['index'] == 'sh600000']