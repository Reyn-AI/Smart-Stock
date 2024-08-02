from typing import Union, Dict, List
import mplfinance as mpf
import pandas as pd
import os
from .base import BaseViewer
from src.utils.common import *
from src.items.enum_item import ApiType
import matplotlib as plt

class MpfPlot(BaseViewer):
    """绘制plot"""
    
    def visual(self, infos: Union[List, pd.DataFrame], **kwargs):
        if isinstance(infos, list):
            infos = tushare_dict_to_df(infos)
        self.save_dir = kwargs.get('save_dir', get_default_output_path())
        return self.do_plot_candle(kl_pd=infos, **kwargs)

    
    def df_rename_tushare(self, df):
        df.rename(columns={'trade_date': 'Date', 'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'vol':'Volume'}, inplace=True)
        df = df.set_index('Date')
        return df
    
    def df_rename_akshare(self, df):
        df = cal_k_mean(df)
        df.rename(columns = {'成交时间': 'Date', '成交价格':'Close', '成交量': 'Volume'
                                  }, inplace=True)
        df['Open'] = df['Close']
        df['High'] = df['Close']
        df['Low'] = df['Close'] 
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        return df
    
    def do_plot_candle(self, kl_pd:pd.DataFrame, exec_type=None, **kwargs):
        """
        绘制不可交互的k线图
        """
        mav = kwargs.get('mav', (3,5, 10))
        if exec_type is None:
            return
        if exec_type == ApiType.TUSHARE:
            kl_pd = self.df_rename_tushare(kl_pd)
        elif exec_type == ApiType.AKSHARE:
            kl_pd = self.df_rename_akshare(kl_pd)
            
        custom_style = mpf.make_mpf_style(base_mpf_style='yahoo', gridstyle='-', y_on_right=False, gridaxis='horizontal')
        save_path = os.path.join(self.save_dir, f'{kl_pd.iloc[0].ts_code}_k_line.png')
        adps = []
        if 'mark_high' in kl_pd:
            high = (kl_pd['mark_high']+0.1).to_list()
            low = (kl_pd['mark_low']-0.1).to_list()
            adp_high = mpf.make_addplot(high, type='scatter', markersize=100, marker='v', color='red')
            adp_low = mpf.make_addplot(low, type='scatter', markersize=100, marker='^', color='green')
            adps.append(adp_high)
            adps.append(adp_low)
        if 'mean' in kl_pd:
            k_mean = kl_pd['mean'].to_list()
            adp = mpf.make_addplot(k_mean, type='line', color='black')
            adps.append(adp)
        mpf.plot(kl_pd, type='candle',
                style=custom_style,
                title=f'{kl_pd.iloc[0].ts_code}',
                volume=True,
                addplot=adps,
                figscale=3,
                savefig=save_path,
                figratio=(5,3),
                fontscale=2,
                scale_padding=1,
                datetime_format='%Y-%m-%d %H:%M:%S')
        print(f'Save in {save_path}')
        return save_path

    