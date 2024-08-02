import requests


ip = '0.0.0.0'
port = 38888
def test_overall_zs():
    url = f"http://{ip}:{port}/overall/zs"
    response = requests.post(url)
    print(response.text)

def test_overall_zt():
    url = f"http://{ip}:{port}/overall/zt"
    response = requests.post(url)
    print(response.text)

def test_overall_hq():
    url = f"http://{ip}:{port}/overall/hq"
    response = requests.post(url)
    print(response.text)

def test_overall_dt():
    url = f"http://{ip}:{port}/overall/dt"
    response = requests.post(url)
    print(response.text)

def test_overall_market():
    url = f"http://{ip}:{port}/overall/market"
    response = requests.post(url)
    breakpoint()
    # print(response.text)
test_overall_market()