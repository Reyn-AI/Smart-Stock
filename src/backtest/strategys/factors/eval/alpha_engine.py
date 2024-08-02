from typing import List
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[5]))
from src.utils.stock_utils import get_day_k_data_multi, get_codes_by_zs_code
import alphalens as al
import pandas as pd

class AlphaLenEngine:
    
    def __init__(self,):
        pass
    
    def format_price_data(self, stock_data, code_name='code', value_name='close'):
        """获取数据"""
        if stock_data is None:
            return stock_data
        stock_data.date = pd.to_datetime(stock_data.date).drop_duplicates()
        price = stock_data.pivot(index=['date'], columns=[code_name], values=value_name)
        return price
    
    def format_factor_data(self, stock_data:pd.DataFrame, factor_name, code_name='code', date_name='date'):
        """获取数据"""
        if stock_data is None:
            return stock_data
        data = stock_data[[code_name, factor_name]]
        data = data.pivot_table(index=[date_name, code_name])
        data.index.set_names(['date', 'asset'])
        return data[factor_name]

    def forward_returns(self, df:pd.DataFrame, factor_name, code_name='code', value_name='close', *args, **kwargs):
        """
            df: 包含因子和加个的dataframe
            factor_name: 因子列名字
            code_name: 股票的列名
            value_name: 价格的列名
            其他参数需要的参数同 get_clean_factor_and_forward_returns
        """
        factors = self.format_factor_data(stock_data=df, code_name=code_name, factor_name=factor_name)
        prices = self.format_price_data(stock_data=df, code_name=code_name, value_name=value_name)
        res = al.utils.get_clean_factor_and_forward_returns(factor=factors, prices=prices, *args, **kwargs)
        return res

if __name__ == '__main__':
    # codes = get_codes_by_zs_code('sz50')
    codes = ['600640', '600641']
    stock_data = get_day_k_data_multi(codes=codes, start_date='2023-05-31', end_date='2024-06-17')
    price = AlphaLenEngine().format_price_data(stock_data=stock_data)
    factors = AlphaLenEngine().format_factor_data(stock_data=stock_data, value_name='volume')
    factor_data = al.utils.get_clean_factor_and_forward_returns(factor=factors, prices=price)
    al.tears.create_returns_tear_sheet(factor_data,
                                   long_short=True,
                                   group_neutral=False,
                                   by_group=True)
    breakpoint()