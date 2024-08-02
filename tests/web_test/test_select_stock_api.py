import requests


ip = '0.0.0.0'
port = 38888
def test_select_strategy_list():
    url = f"http://{ip}:{port}/select_stocks/strategy_list"
    response = requests.post(url)
    print(response.text)
    
def test_select_market():
    url = f"http://{ip}:{port}/select_stocks/marget_list"
    response = requests.post(url)
    print(response.text)

def test_select_market():
    url = f"http://{ip}:{port}/select_stocks/marget_list"
    response = requests.post(url, data={})
    print(response.text)

def get_selected_stock_data():
    url = f"http://{ip}:{port}/select_stocks/get_selected_stock_data"   
    data = {"strategyParams": [{"code": 'TuShareDataAnalysis', "paramList": []},
                               {"code": 'TuShareDataAnalysisZFltn', "paramList": [{'code':'threshold', 'default':5}]},
                               {"code": 'AkShareThsSpecialStocks',  "paramList": [{'code':'how', 'default':['cxg']}]}
                               ],
            "marketParams": ['1', '2']}
    response = requests.post(url, json=data)
    print(response.json())

def test_day_kline():
    url = f"http://{ip}:{port}/kline/day"
    data = {'code':'430017',
            'nYear': 2,
            'support':True}
    response = requests.post(url, json=data)
    print(response.json()['supportData'])


def test_select_by_history():
    url = f"http://{ip}:{port}/select_stocks/get_selected_stock_data_by_history"
    data = {"strategyParams": [{'name':'窗口时间内走势角度选股策略','code':'TaLibDataAnalysisSelectByAngle', 'params':[{'code':'timeperiod', 'name':"窗口长度", 'default':10, 'uiType':'input'},
                                            {'code':'angle', 'name':"角度阈值", 'default':1, 'uiType':'input'},
                                            {'name':'k线类型', 'code':'frequency', 'default':'d', 'uiType':'select'},
                                            {'code':'startDate', 'name':'开始日期', 'uiType':'date', 'default':'2024-01-01'},
                                             {'code':'endDate', 'name':'结束日期', 'uiType':'date', 'default':'2025-01-01'}]}
                               ],
            "marketParams": ['1', '2']}
    response = requests.post(url, json=data)
    print(response.json())

test_select_by_history()