import requests

# ip = '139.159.177.235'
ip = '0.0.0.0'
port = 38888
def test_add_order():
    url = f"http://{ip}:{port}/order/add_order"
    params = {
        'userID':'19850160511',
        'stockName':'国脉文化',
        'tradeDate': '2024-04-04 09:12:01',
        'volume':100,
        'price':14.98,
        'stockStatus':1
    }
    response = requests.post(url, json=params)
    print(response.text)

def test_update_order():
    url = f"http://{ip}:{port}/order/update_order"
    params = {
        'userID':'19850160511',
        'stockName':'国脉文化',
        'tradeDate': '2024-04-24 09:12:01',
        'volume':1000,
        'price':12.98,
        'stockStatus':0,
        'id':1
    }
    response = requests.post(url, json=params)
    print(response.text)

def test_delete_order():
    url = f"http://{ip}:{port}/order/delete_order"
    params = {
        'userID':'19850160511',
        'id':1
    }
    response = requests.post(url, json=params)
    print(response.text)

def test_select_order():
    url = f"http://{ip}:{port}/order/select_order"
    params = {
        'userID':'19850160511',
        'stockName':'国脉文化'
    }
    response = requests.post(url, json=params)
    print(response.text)

def test_select_order_and_analysis():
    url = f"http://{ip}:{port}/order/select_order_and_analysis"
    params = {
        'userID':'19850160511',
    }
    response = requests.post(url, json=params)
    print(response.text)
test_select_order()