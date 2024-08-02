import requests

# ip = '139.159.177.235'
ip = '0.0.0.0'
port = 38888
def test_get_base_infos():
    url = f"http://{ip}:{port}/stock_infos/get_base_infos"
    params = {
        'code':'600640'
    }
    response = requests.post(url, json=params)
    print(response.text)

test_get_base_infos()