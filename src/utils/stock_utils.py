import concurrent.futures
from typing import List, Dict, Union
import pandas as pd
import numpy as np
from src.view.mpf_plot import MpfPlot
import abc
from src.utils.common import *
from src.api.baostock_executor import BaoStockExecutor
from src.backtest.tushare_feed import TuSharePandasFeed
import concurrent
from functools import partial
import qstock as qs
from functools import lru_cache
from multiprocessing import cpu_count


def get_codes_by_zs_code(code):
    """根据指数获取成分股
        code: sz50(上证50)、hs300、zz500、zz1000、kc50
    """
    df=qs.index_member(code)
    codes = df['股票代码'].tolist()
    return codes

@lru_cache
def get_all_market_codes(name='沪深京A'):
    """获取全市场股票名"""
    try:
        df=qs.realtime_data(name)
        res = df['代码'].tolist()
        return res
    except Exception as e:
        return None


class BaseCalculate(metaclass=abc.ABCMeta):
    """基础计算类"""
    
    def __init__(self,
                 save_dir=get_default_output_path(),
                 *args,
                 **kwargs):
        self.save_dir = save_dir
        self.args = args
        self.kwargs = kwargs
        
    abc.abstractmethod
    def calculate(self, infos:Union[List, pd.DataFrame], **kwargs):
        pass

class CalHighLowPoint(BaseCalculate):
    """计算k先买卖高低点"""
    
    def calculate(self, infos:Union[List, pd.DataFrame], **kwargs):
        """k线计算"""
        if isinstance(infos, list):
            infos = tushare_dict_to_df(infos)
            
        res = self.enter_main(infos)
        infos['mark_low'] = np.nan
        infos['mark_high'] = np.nan
        index = [x[0] for x in res]
        mark = [x[2] for x in res]
        for i, m in zip(index, mark):
            if m:
                df.loc[i, 'mark_high'] = df.loc[i, 'high']
            else:
                df.loc[i, 'mark_low'] = df.loc[i, 'low']
        if kwargs.get('visual'):
            return MpfPlot().visual(infos=df, save_dir=self.save_dir)
        return infos
    
    def caculate_turning_point(self, pre_df,start_x,y_col,x_col, mark):
        '''
        计算转折点
        :param pre_df: 要计算的数据
        :param start_x: 起点
        :param y_col: y的列名
        :param x_col: x的列名
        :param mark:True=峰 False=谷
        :return: 第一个转折点 [x_val,y_val,mark]
        '''
        df = pre_df.loc[pre_df[x_col]<start_x-3].copy() #如果上一个点是最高/低点则次高点最少距离3天
        if mark:
            # 峰值
            df['p0'] = df[y_col].cummax()
            df['p1'] = df['p0'] - df['p0'].shift(1)
            df['p2'] = 1
            df.loc[df['p1'] != 0, 'p2'] = 0
            df['p3'] = 0
            df.loc[(df['p2'] == 0) & (df['p2'].shift(-1) == 1), 'p3'] = 1
            df['p4'] = 0 #是连续3条k线中的最高的置为 1
            df_p = df.loc[(df['p3']==1) & (df['p2'].shift(-2) == 1) & (df['p2'].shift(-3) == 1), 'p4'] = 1
            df_p = df.loc[df['p4']==1].copy()
            if len(df_p)<=0:
                return [None,None,mark]
            else:
                p_i = df_p.iloc[0][x_col]
                p_y = df_p.iloc[0][y_col]
                return [p_i,p_y,mark]
        else:
            # 谷值
            df['l0'] = df[y_col].cummin()
            df['l1'] = df['l0'] - df['l0'].shift(1)
            df['l2'] = 1
            df.loc[df['l1'] != 0, 'l2'] = 0
            df['l3'] = 0
            df.loc[(df['l2'] == 0) & (df['l2'].shift(-1) == 1), 'l3'] = 1
            df['l4'] = 0
            df.loc[(df['l2'] == 0) & (df['l2'].shift(-1) == 1)& (df['l2'].shift(-2) == 1)& (df['l2'].shift(-3) == 1), 'l4'] = 1
            df_l = df.loc[df['l4'] == 1].copy()
    
            if len(df_l) <= 0:
                return [None, None, mark]
            else:
                l_i = df_l.iloc[0][x_col]
                l_y = df_l.iloc[0][y_col]
                return [l_i, l_y, mark]

    def circle_find(self, start_mark,i_start,pre_df,py_col,ly_col,x_col)->List:
        res_list = []
        i = i_start
        while True:
            if i<=0:
                break
            if start_mark:
                # 峰值
                res_one = self.caculate_turning_point(pre_df,i,py_col,x_col,start_mark)
            else:
                # 谷值
                res_one = self.caculate_turning_point(pre_df,i,ly_col,x_col,start_mark)
            if not res_one[0]:
                break
            res_list.append(res_one)
            i = res_one[0]
            start_mark = not start_mark
        return res_list

    def enter_main(self, df):
        # 1 截取要计算的时间区间对应的日数据
        df = df.loc[df['open']>0].copy()
    
        # 2 逆序，并设置索引字段
        df['i_row'] = [i for i in range(len(df))]
        i_row_list = df['i_row'].values.tolist()
        i_row_list.reverse()
        df['i_row_r'] = i_row_list
        h_list = df['high'].values.tolist()
        h_list.reverse()
        df['hr'] = h_list
        l_list = df['low'].values.tolist()
        l_list.reverse()
        df['lr'] = l_list
    
        # 3 从最新日期往前寻找所有转折点，即所有的峰谷值
        res_list = []
        i_len = len(i_row_list)
        p_first = self.caculate_turning_point(df,i_len,'hr','i_row_r',True)
        l_first = self.caculate_turning_point(df,i_len,'lr','i_row_r',False)
        if p_first[0]<l_first[0]:
            # 第一个
            res_list.append(l_first)
            res_list.append(p_first)
            # 谷开始
            res_list00 = self.circle_find(False, p_first[0], df, 'hr', 'lr', 'i_row_r')
        else:
            # 第一个
            res_list.append(p_first)
            res_list.append(l_first)
            # 峰开始
            res_list00 = self.circle_find(True, l_first[0], df, 'hr', 'lr', 'i_row_r')
    
        res_list.extend(res_list00)
        df_pv = pd.DataFrame(columns=['x','y','mark'],data=res_list)
    
        return df_pv.loc[:,['x','y', 'mark']].values.tolist()


    # mpf.make_addplot()
    
def calc_atr(kline_df):
    """
    为输入的kline_df金融时间序列计算atr21和atr14，计算结果直接加到kline_df的atr21列和atr14列中
    :param kline_df: 金融时间序列pd.DataFrame对象
    """
    kline_df['atr21'] = 0
    if kline_df.shape[0] > 21:
        # 大于21d计算atr21
        kline_df['atr21'] = Atr.atr21(kline_df['high'].values, kline_df['low'].values, kline_df['pre_close'].values)
        # 将前面的bfill
        kline_df['atr21'].fillna(method='bfill', inplace=True)
    kline_df['atr14'] = 0
    if kline_df.shape[0] > 14:
        # 大于14d计算atr14
        kline_df['atr14'] = Atr.atr14(kline_df['high'].values, kline_df['low'].values, kline_df['pre_close'].values)
        # 将前面的bfill
        kline_df['atr14'].fillna(method='bfill', inplace=True)

def calc_start_end_date(n_folds, start=None, end=None):
    """
    根据参数计算start，end
    :param df: 本地缓存的金融时间序列对象，pd.DataFrame对象
    :param force_local: 是否强制走本地数据
    :param n_folds: 需要几年的数据
    :param start: 开始的时间
    :param end: 结束的时间
    :return:
    """
    from abupy import ABuDateUtil

    # 当前今天时间日期str对象，如果是强制本地，即缓存的最后一个交易日
    today =ABuDateUtil.current_str_date()
    if end is None:
        # 没有end也没start，end＝today，否则使用n_folds计算end
        end = today if start is None else ABuDateUtil.begin_date(-365 * n_folds, date_str=start, fix=False)
    # int类型的end, today转换
    end_int = ABuDateUtil.date_str_to_int(end)
    today_int = ABuDateUtil.date_str_to_int(today)
    if end_int > today_int:
        end_int = today_int

    if start is None:
        start = ABuDateUtil.begin_date(365 * n_folds, date_str=end, fix=False)
    start_int = ABuDateUtil.date_str_to_int(start)
    return start_int, end_int

import akshare as ak
from src.api.txapi import TXApi

def get_day_k_data(code, 
                   n_folds=1,
                   start_date=None,
                   end_date=None,
                   api_type='qstock',
                   frequency='d',
                   *args,
                   **kwargs):
    """获取日线数据"""
    if kwargs.get('frequency', 'd') != 'd':
        api_type =='qstock'
    if api_type == 'qstock':
        """freq:时间频率，默认日，1 : 分钟；5 : 5 分钟；15 : 15 分钟；30 : 30 分钟； 60 : 60 分钟；101或'D'或'd'：日；102或‘w’或'W'：周; 103或'm'或'M': 月 注意1分钟只能获取最近5个交易日一分钟数据"""
        if start_date is None and end_date is None:
                start, end = calc_start_end_date(n_folds=n_folds)
        else:
            start = start_date.replace('-', '')
            end = end_date.replace('-', '')
        if frequency.isnumeric():
            frequency = int(frequency)
        df = qs.get_data(code, start=str(start), end=str(end), freq=frequency)
        if df is None:
            return df
        df = df.rename(columns={'vol':'volume'})
        df['date'] = pd.to_datetime(df.index)
        df['date'] = df.date.apply(lambda x:x.strftime('%Y-%m-%d %H:%M'))
        return df
    elif api_type !='baostock':
        if not code.startswith(('60','0')):
            #非主板走akshare接口
            if start_date is None and end_date is None:
                start, end = calc_start_end_date(n_folds=n_folds)
            else:
                start = start_date.replace('-', '')
                end = end_date.replace('-', '')
            df = ak.stock_zh_a_hist(symbol=code, start_date=start, end_date=end)
            df = df.rename(columns={'日期':'date', '开盘':'open', '收盘':'close',
                                    '最高':'high', '最低':'low', '成交量':'volume', '成交额':'account'})
            # df = df[['date', 'open','close', 'high', 'low', 'volume']]
        else:
            code = code_to_abu_code(code)
            df = TXApi().kline(symbol=code, n_folds=n_folds, start=start_date, end=end_date)
            if df is None:
                return df
            df.date = df.date.apply(fmt_date)
        return df
    else:
        if start_date is None or end_date is None or start_date=='' or end_date=='':
            start_date, end_date = calc_start_end_date(n_folds=n_folds)
        start_date = fmt_date(start_date)
        end_date = fmt_date(end_date)
        df = BaoStockExecutor().get_history_time_data(code=code,
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 **kwargs)
        return df

def get_real_time_data(api_type='qstock', return_dict=False):
    df = None
    if api_type=='qstock':
        df=qs.realtime_data()
    if return_dict:
        df = dftodict(df)
    return df


def staistics_zdt_group(group_info=[-7, -5, -3, 0, 3, 5, 7], zdf_key='涨幅'):
    """统计实时数据涨跌幅"""
    df = get_real_time_data()
    res = {}
    for i in group_info:
        if i<=0:
            r = df[df[zdf_key]<=i]
            res[f'涨幅小于{i}%数量'] = len(r)
        if i>=0:
            r = df[df[zdf_key]>=i]
            res[f'涨幅大于{i}%数量'] = len(r)
        
    return res, df

def get_day_k_data_multi(codes:List, 
                   n_folds=1,
                   start_date=None,
                   end_date=None,
                   api_type='qstock',
                   max_workers=20,
                   return_list=False,
                   frequency='d',
                   *args,
                   **kwargs):
    results = []
    if api_type == 'qstock':
        """freq:时间频率，默认日，1 : 分钟；5 : 5 分钟；15 : 15 分钟；30 : 30 分钟； 60 : 60 分钟；101或'D'或'd'：日；102或‘w’或'W'：周; 103或'm'或'M': 月 注意1分钟只能获取最近5个交易日一分钟数据"""
        if start_date is None and end_date is None:
                start, end = calc_start_end_date(n_folds=n_folds)
        else:
            start = start_date.replace('-', '')
            end = end_date.replace('-', '')
        if frequency.isnumeric():
            frequency = int(frequency)
        df = qs.get_data(codes, start=str(start), end=str(end), freq=frequency)
        if df is None:
            return df
        df = df.rename(columns={'vol':'volume'})
        df['date'] = pd.to_datetime(df.index)
        if return_list:
            df_group = df.groupby('name')
            results = [x[1] for x in df_group]
            return results
        else:
            return df
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        func = partial(get_day_k_data, n_folds=n_folds, start_date=start_date,end_date=end_date,api_type=api_type)
        future_to_result = [executor.submit(func, code)  for code in codes]
        for future in concurrent.futures.as_completed(future_to_result):
            try:
                data = future.result()
                results.append(data)
            except Exception as e:
                print(f'{future} generated an exception: {e}')
    if not return_list:
        return pd.concat(results)
    return results

def backtrader_add_data_by_k_type(cerebro, code, start_date, end_date, frequency='d'):
    """从tushare 添加回测数据"""
    st_date = time_str_to_datetime(start_date)
    ed_date = time_str_to_datetime(end_date)
    df = get_day_k_data(code=code, start_date=st_date, end_date=ed_date, api_type='baostock', frequency=frequency)
    # 添加 600276.SH 的行情数据
    datafeed1 = TuSharePandasFeed(dataname=df, fromdate=st_date, todate=ed_date)
    cerebro.adddata(datafeed1, name=f"{code}_{frequency}")
    return datafeed1


def cal_exist_zt_in_windows(df:pd.DataFrame, windows=10):
    """计算窗口时间内是否存在涨停"""
    def judge_zt(x):
        #10cm涨停
        zt10 = abs(x-0.1)<0.005
        #20cm涨停
        zt20 = abs(x-0.2)<0.005
        flag = zt10 | zt20
        return flag.any()
    
    if not isinstance(df, pd.DataFrame):
        raise RuntimeError
    df['change'] = df['close'].rolling(window=2).apply(lambda x: round((float(x[-1]) - float(x.iloc[0]))/float(x.iloc[0]),4))
    df['exist_zt'] = df['change'].rolling(window=windows).apply(judge_zt)
    return df

if __name__ == '__main__':
    res =  get_day_k_data_multi(start_date='2024-05-07', end_date='2024-07-30', codes=['600460'])
    res = cal_exist_zt_in_windows(res)
    print(res)