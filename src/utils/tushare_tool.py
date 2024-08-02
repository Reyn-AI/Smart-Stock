import pandas as pd
import tushare as ts
from src.utils.common import *
import datetime
from src.backtest.tushare_feed import TuSharePandasFeed
from src.utils.stock_utils import get_day_k_data
from src.api.baostock_executor import BaoStockExecutor
import qstock as qs

def get_data_by_tushare(code,start_date, end_date):
    """从tushare获取回测数据"""
    code = format_ts_code([code])[0]
    start_date = start_date.replace('-','')
    end_date = end_date.replace('-','')
    df = ts.pro_bar(ts_code=code, adj='qfq',start_date=start_date, end_date=end_date)
    df = df[['trade_date', 'open', 'high', 'low', 'close', 'vol', 'pre_close', 'change', 'pct_chg', 'amount']]
    df.rename(columns={'vol':'volume'}, inplace=True)
    columns =  ['trade_date', 'open', 'high', 'low', 'close', 'volume', 'pre_close', 'change']
    df.trade_date = pd.to_datetime(df.trade_date)
    df.index = df.trade_date
    df.sort_index(inplace=True)
    df.fillna(0.0,inplace=True)
    df = df[columns]

    return df

def backtrader_add_data_from_tushare(cerebro, code, start_date, end_date, api_type='qstock'):
    """从tushare 添加回测数据"""
    if api_type =='tushare':
        df = get_data_by_tushare(code, start_date, end_date)
    elif api_type=='abu':
        df = get_data_by_abu(code=code, start_date=start_date, end_date=end_date)
    elif api_type=='bao':
        df = get_data_from_bao_stock(code=code, start_date=start_date, end_date=end_date)
    elif api_type=='qstock':
        df = get_data_from_q_stock(code=code, start_date=start_date, end_date=end_date)
    df.replace(0, -1, inplace=True)
    st_date = time_str_to_datetime(start_date)
    ed_date = time_str_to_datetime(end_date)
    # 添加 600276.SH 的行情数据
    datafeed1 = TuSharePandasFeed(dataname=df, fromdate=st_date, todate=ed_date)
    cerebro.adddata(datafeed1, name=code)
    return datafeed1

def get_data_from_bao_stock(code, start_date, end_date):
    df = BaoStockExecutor().get_history_time_data(code=code, start_date=start_date, end_date=end_date)
    df.fillna(-1,inplace=True)
    df.rename(columns={'preclose':'pre_close', 'pctChg':'change'}, inplace=True)
    columns = ['open', 'high', 'low', 'close', 'volume', 'pre_close', 'change']
    for col in columns:
        try:
            df[col] = df[col].astype(float)
        except Exception as e:
            df[df[col]==''] = 0
            df[col] = df[col].astype(float)
    return df

def get_data_from_q_stock(code, start_date, end_date, freq='d'):
    start_date = start_date.replace('-','')
    end_date = end_date.replace('-','')
    df = qs.get_data(code, start=start_date, end=end_date, freq=freq)
    df.fillna(-1,inplace=True)
    columns = ['open', 'high', 'low', 'close', 'volume']
    for col in columns:
        try:
            df[col] = df[col].astype(float)
        except Exception as e:
            df[df[col]==''] = 0
            df[col] = df[col].astype(float)
    return df

# def get_data_by_abu(code,start_date, end_date):
#     from abupy import ABuSymbolPd
#     code = code_to_abu_code(code)
#     df = ABuSymbolPd.make_kl_df(symbol=code, start=start_date, end=end_date)
#     if df is None:
#         return None
#     df.fillna(0.0,inplace=True)
#     df.rename(columns={'p_change':'change'}, inplace=True)
#     columns = ['open', 'high', 'low', 'close', 'volume', 'pre_close', 'change']
#     df = df[columns]
#     return df

def get_data_by_abu(code,start_date, end_date):
    from src.api.txapi import TXApi
    df = TXApi().kline(symbol=code, start=start_date, end=end_date)
    if df is None:
        return None
    df.fillna(0.0,inplace=True)
    df.rename(columns={'p_change':'change'}, inplace=True)
    columns = ['open', 'high', 'low', 'close', 'volume', 'pre_close', 'change']
    df = df[columns]
    return df

if __name__ == '__main__':
    res = get_data_by_abu(code='600001', start_date='2019-01-03', end_date='2024-04-01')
    # res1 = get_data_by_abu1(code='600640', start_date='2019-01-03', end_date='2024-04-01')
