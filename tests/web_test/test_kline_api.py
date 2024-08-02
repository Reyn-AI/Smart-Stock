import requests

ip = '0.0.0.0'
port = 38888
def test_get_kline():
    url = f"http://{ip}:{port}/kline/kline_by_freq"
    params = {
        'code':'600640',
        'frequency':'5',
        'startDate':'2024-05-07',
        'endDate': '2024-05-09'
    }
    response = requests.post(url, json=params)
    print(response.text)

test_get_kline()