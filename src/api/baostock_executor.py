from typing import List, Dict
from src.api.base import BaseExecutor
from src.utils.common import *
from src.utils.parallel_util import *
from src.crawls.sina_crawl import *
import pandas as pd
import pandas as pd
import baostock as bs
from src.utils.constant import BAO_STOCK_NAME
from concurrent.futures import ThreadPoolExecutor
from functools import partial

@singleeton_func
class BaoStockExecutor(BaseExecutor):
    
    def __init__(self, api_name: str='BaoStock', save_dir: str = None, *args, **kwargs):
        super().__init__(api_name, save_dir, *args, **kwargs)
        bs.login()
    
    def get_history_time_data(self, *args, **kwargs):
        """获取单个股票历史数据
            Args:
                return_list df转为list
                codes: 股票代码如 sh.xxxxxx
                start: 开始日期（包含），格式“YYYY-MM-DD”，为空时取2015-01-01；
                end：结束日期（包含），格式“YYYY-MM-DD”，为空时取最近一个交易日；
                frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写
                adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权。
        """
        code = kwargs.get('code')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        frequency = kwargs.get('frequency', 'd')
        adjustflag = kwargs.get('adjustflag', '3')
        return_list = kwargs.get('return_list', False)
        code = code_to_bao_code(code)
        if frequency.lower() == 'd':
            #日线
            fields = "date,code,pctChg,open,high,low,close,preclose,volume,turn,amount,peTTM,psTTM,pcfNcfTTM,pbMRQ"
            
        elif frequency.lower() in ['w', 'm']:
            #周线
            fields = "date,code,pctChg,open,high,low,close,volume,amount,turn,pctChg"
        
        elif frequency.lower() in ['5', '15', '30', '60']:
            #分时
            fields = "date,time,code,open,high,low,close,volume,amount,adjustflag"
        rs = bs.query_history_k_data_plus(code,
                                          fields,
                                          start_date=start_date,
                                          end_date=end_date,
                                          frequency=frequency,
                                          adjustflag=adjustflag)
        df = self.from_rs_get_df(rs, return_list=False)
        if 'time' in df:
            df['time'] = df['time'].apply(fmt_time)
            df['date'] = df['time']
        if return_list:
            df = dftodict(df)
            return df
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date', drop=False)
        return df
        
    
    async def get_base_data(self, *args, **kwargs):
        """获取基本面数据"""
        res = {}
        res['盈利能力'] = self.get_base_infos_dispatch(bs.query_profit_data, *args, **kwargs)
        res['营运能力'] = self.get_base_infos_dispatch(bs.query_operation_data, *args, **kwargs)
        # res['偿债能力'] = self.get_base_infos_dispatch(bs.query_balance_data, *args, **kwargs)
        # res['现金流能力'] = self.get_base_infos_dispatch(bs.query_cash_flow_data, *args, **kwargs)
        res['杜邦指数'] = self.get_base_infos_dispatch(bs.query_dupont_data, *args, **kwargs)
        res['成长能力'] = self.get_base_infos_dispatch(bs.query_growth_data, *args, **kwargs)
        # res['公司业绩快报'] = self.get_query_performance_express_report(*args, **kwargs)
        return res
            
    def from_rs_get_df(self, rs, return_list=True, type2str=True):
        """获取df数据"""
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields).fillna('N/A')
        if not return_list:
            return result
        res = dftodict(result)
        if type2str:
            res = self.type2str(res, type_str_dict=BAO_STOCK_NAME)
        return res    
    
    def get_base_infos_dispatch(self, func, *args, **kwargs):
        """并行分发"""
        print(func)
        code = kwargs.get('code')
        code = code_to_bao_code(code)
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        return_list = kwargs.get('return_list', True)
        if quarter is None:
            codes = [code]*4
            years = [year]*4
            quarters = [1,2,3,4]
            with ThreadPoolExecutor(max_workers=1) as executor:
                results = executor.map(func, codes,years, quarters)
            df_res = []
            for res in results:
                df_ = self.from_rs_get_df(res, return_list=False)
                df_res.append(df_)
            df = pd.concat(df_res, ignore_index=True)
            if return_list:
                df = dftodict(df)
                df = self.type2str(df, type_str_dict=BAO_STOCK_NAME)
        else:
            rs_profit = func(code=code, year=year, quarter=quarter)
            df = self.from_rs_get_df(rs_profit, return_list=return_list)
        return df
    
    async def get_query_profit_data(self, *args, **kwargs):
        """查询季频盈利能力
            Args:
                code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
                year：统计年份，为空时默认当前年；
                quarter：统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = kwargs.get('code')
        code = code_to_bao_code(code)
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        return_list = kwargs.get('return_list', True)
        df_res = []
        if quarter is None:
            for q in [1,2,3,4]:
                rs_profit = bs.query_profit_data(code=code, year=year, quarter=q)
                df1 = self.from_rs_get_df(rs_profit, return_list=False)
                df_res.append(df1)
            df = pd.concat(df_res, ignore_index=True)
            if return_list:
                df = dftodict(df)
                df = self.type2str(df, type_str_dict=BAO_STOCK_NAME)
        else:
            rs_profit = bs.query_profit_data(code=code, year=year, quarter=quarter)
            df = self.from_rs_get_df(rs_profit, return_list=return_list)
        return df
    
    async def get_query_operation_data(self, *args, **kwargs):
        """查询季频营运能力
            Args:
                code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
                year：统计年份，为空时默认当前年；
                quarter：统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = kwargs.get('code')
        code = code_to_bao_code(code)
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        quarter = kwargs.get('quarter')
        return_list = kwargs.get('return_list', True)
        df_res = []
        if quarter is None:
            for q in [1,2,3,4]:
                rs_profit = bs.query_operation_data(code=code, year=year, quarter=q)
                df1 = self.from_rs_get_df(rs_profit, return_list=False)
                df_res.append(df1)
            df = pd.concat(df_res, ignore_index=True)
            if return_list:
                df = dftodict(df)
                df = self.type2str(df, type_str_dict=BAO_STOCK_NAME)
        else:
            rs_profit = bs.query_operation_data(code=code, year=year, quarter=quarter)
            df = self.from_rs_get_df(rs_profit, return_list=return_list)
        return df
    
    async def get_query_growth_data(self, *args, **kwargs):
        """查询季频成长能力
            Args:
                code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
                year：统计年份，为空时默认当前年；
                quarter：统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = kwargs.get('code')
        code = code_to_bao_code(code)
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        return_list = kwargs.get('return_list', True)
        df_res = []
        if quarter is None:
            for q in [1,2,3,4]:
                rs_profit = bs.query_growth_data(code=code, year=year, quarter=q)
                df1 = self.from_rs_get_df(rs_profit, return_list=False)
                df_res.append(df1)
            df = pd.concat(df_res, ignore_index=True)
            if return_list:
                df = dftodict(df)
                df = self.type2str(df, type_str_dict=BAO_STOCK_NAME)
        else:
            rs_profit = bs.query_growth_data(code=code, year=year, quarter=quarter)
            df = self.from_rs_get_df(rs_profit, return_list=return_list)
        return df
    
    async def get_query_balance_data(self, *args, **kwargs):
        """查询季频偿债能力
            Args:
                code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
                year：统计年份，为空时默认当前年；
                quarter：统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = kwargs.get('code')
        code = code_to_bao_code(code)
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        return_list = kwargs.get('return_list',True)
        df_res = []
        if quarter is None:
            for q in [1,2,3,4]:
                rs_profit = bs.query_balance_data(code=code, year=year, quarter=q)
                df1 = self.from_rs_get_df(rs_profit, return_list=False)
                df_res.append(df1)
            df = pd.concat(df_res, ignore_index=True)
            if return_list:
                df = dftodict(df)
                df = self.type2str(df, type_str_dict=BAO_STOCK_NAME)
        else:
            rs_profit = bs.query_balance_data(code=code, year=year, quarter=quarter)
            df = self.from_rs_get_df(rs_profit, return_list=return_list)
        return df
    
    async def get_query_cash_flow_data(self, *args, **kwargs):
        """查询季频现金流能力
            Args:
                code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
                year：统计年份，为空时默认当前年；
                quarter：统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = kwargs.get('code')
        code = code_to_bao_code(code)
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        return_list = kwargs.get('return_list',True)
        df_res = []
        if quarter is None:
            for q in [1,2,3,4]:
                rs_profit = bs.query_cash_flow_data(code=code, year=year, quarter=q)
                df1 = self.from_rs_get_df(rs_profit, return_list=False)
                df_res.append(df1)
            df = pd.concat(df_res, ignore_index=True)
            if return_list:
                df = dftodict(df)
                df = self.type2str(df, type_str_dict=BAO_STOCK_NAME)
        else:
            rs_profit = bs.query_cash_flow_data(code=code, year=year, quarter=quarter)
            df = self.from_rs_get_df(rs_profit, return_list=return_list)
        return df
    
    async def get_query_dupont_data(self, *args, **kwargs):
        """查询季频杜邦指数
            Args:
                code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
                year：统计年份，为空时默认当前年；
                quarter：统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = kwargs.get('code')
        code = code_to_bao_code(code)
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        return_list = kwargs.get('return_list', True)
        df_res = []
        if quarter is None:
            for q in [1,2,3,4]:
                rs_profit = bs.query_dupont_data(code=code, year=year, quarter=q)
                df1 = self.from_rs_get_df(rs_profit, return_list=False)
                df_res.append(df1)
            df = pd.concat(df_res, ignore_index=True)
            if return_list:
                df = dftodict(df)
                df = self.type2str(df, type_str_dict=BAO_STOCK_NAME)
        else:
            rs_profit = bs.query_dupont_data(code=code, year=year, quarter=quarter)
            df = self.from_rs_get_df(rs_profit, return_list=return_list)
        return df

    def get_query_performance_express_report(self, *args, **kwargs):
        """季频公司业绩快报
            Args:
                code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
                start_date：统计年份，为空时默认当前年；
                end_date：统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = kwargs.get('code')
        code = code_to_bao_code(code)
        start_date = kwargs.get('start_date', '2015-01-01')
        end_date = kwargs.get('end_date')
        return_list = kwargs.get('return_list', True)
        rs_forecast = bs.query_performance_express_report(code, start_date=start_date, end_date=end_date)
        return self.from_rs_get_df(rs_forecast, return_list=return_list)

    def get_query_all_stock(self):
        """获取所有股票代码"""
        rs = bs.query_all_stock()
        df = self.from_rs_get_df(rs, return_list=False)
        return df['code'].to_list()

    
if __name__ == '__main__':
    a = BaoStockExecutor()
    res = a.get_history_time_data(code='sh.000001', start_date='2017-01-01', end_date='2024-05-27')
    print(res)
