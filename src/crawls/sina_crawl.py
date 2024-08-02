import requests
import pandas as pd
import json

def stock_zh_a_minute(
        symbol: str = "sh600519", period: str = "1"
) -> pd.DataFrame:
    """
    获取当日k-min数据
    https://finance.sina.com.cn/realstock/company/sh600519/nc.shtml
    :param symbol: sh000300
    :type symbol: str
    :param period: 1, 5, 15, 30, 60 分钟的数据
    :type period: str
    :return: specific data
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/cn/api/jsonp_v2.php/=/CN_MarketDataService.getKLineData"
    params = {
        "symbol": symbol,
        "scale": period,
        "ma": "no",
        "datalen": "238",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    try:
        data_json = json.loads(data_text.split("=(")[1].split(");")[0])
        temp_df = pd.DataFrame(data_json).iloc[:, :6]
    except:
        url = f"https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_{symbol}_{period}_1658852984203=/CN_MarketDataService.getKLineData"
        params = {
            "symbol": symbol,
            "scale": period,
            "ma": "no",
            "datalen": "1970",
        }
        r = requests.get(url, params=params)
        data_text = r.text
        if len(data_text.split("=("))==0:
            print(data_text)
            return pd.DataFrame()
        data_json = json.loads(data_text.split("=(")[1].split(");")[0])
        temp_df = pd.DataFrame(data_json).iloc[:, :6]
    if temp_df.empty:
        print(f"{symbol} 股票数据不存在，请检查是否已退市")
        return pd.DataFrame()
    temp_df['close'] = temp_df['close'].astype(float)
    temp_df['high'] = temp_df['high'].astype(float)
    temp_df['low'] = temp_df['low'].astype(float)
    temp_df['volume'] = temp_df['volume'].astype(float)
    return temp_df

    