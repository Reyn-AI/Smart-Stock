import urllib.request
import numpy as np
import pandas as pd
import json
import time
import asyncio
import matplotlib.pyplot as plt

from datetime import datetime


# // 请求茅台数据为例
# https://web.ifzq.gtimg.cn/appstock/app/minute/query?code=sh600519


# 获取当前时间
def currtime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_currday():
    day = datetime.now().strftime('%d')
    return int(day)

def get_pre5days_stock_closes(stock :str):
    '''
    1.获取的是分钟
    2.获取过去4天的分钟数的所有close

    retrun : [closes]
    '''
    url = r'https://web.ifzq.gtimg.cn/appstock/app/day/query?code=' + stock
    content = json.loads(httpGet(url=url))

    content = content['data'][stock]['data']
    close_lst :list = [float(line.split(' ')[1]) for i in range(len(content)) for line in content[i]['data']]
    breakpoint()
    # print(len(close_lst))
    return close_lst 

def httpGet(url):
    req = urllib.request.Request(url=url)
    content = urllib.request.urlopen(req).read().decode('utf-8')
    return content

def get_minutes_stock_closes(stock: str):
    '''
    1.获取的是分钟
    2.return : [closes]
    '''
    url = r'https://web.ifzq.gtimg.cn/appstock/app/minute/query?code=' + stock
    content = json.loads(httpGet(url=url))
    data_clear :dict = content['data'][stock]['data']
    # line: 0931 1688.46 421 71074270.00
    close_list :list = [float(line.split(' ')[1]) for line in data_clear['data']]

    return close_list

def get_stock_name(stock: str):
    url = r'https://web.ifzq.gtimg.cn/appstock/app/minute/query?code=' + stock
    content = json.loads(httpGet(url=url))
    qt_clear :dict = content['data'][stock]['qt']

    name :str = qt_clear[stock][1]
    code :str = qt_clear[stock][2]
    print(name, code)


def plt_model(stock :str):
    fig = plt.figure(figsize=(9,6))

    close_sz: list = [] # 上证指数

    while True:
        now = currtime()
        print(now)
        if str(now[-2:]) == '00':
            # step1. 获取数据
            close_sz = get_minutes_stock_closes(stock)

        else:
            # step2. 画图
            plt.ion()  # 打开交互模式

            x = np.arange(0, len(close_sz), 1)
            y = [c for c in close_sz]

            plt.clf() # 清空数据
            plt.plot(x, y, label=stock)
            plt.xticks(np.arange(0, len(close_sz), 5))
            plt.xlabel('minutes')
            plt.grid(axis="y", linestyle='--')
            plt.legend(loc=3)

            plt.pause(0.01) # 暂停一段时间，不然画的太快会卡住显示不出来
            plt.ioff()      # 关闭交互模式
    
        time.sleep(1)

if __name__ == '__main__':
    get_pre5days_stock_closes('sh000001')