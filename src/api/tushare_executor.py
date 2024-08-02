from typing import Dict, List, Union
from src.api.base import BaseExecutor
import tushare as ts
from src.utils.constant import TUSHARE_TOKEN
from src.items.tushare_item import TuShareRealTimeQuoteItem, TuShareDailyDataItem
import pandas as pd
from src.utils.common import *
from src.utils.env import *
from src.utils.tushare_constant import *
from src.database.mongodb_utils import MongoDBUtil
import os
from src.utils.env import *
from tqdm import tqdm
from copy import deepcopy
# try:
#     from abupy import ABuSymbolPd
#     ABUPY = True
# except Exception:
#     ABUPY = False

class TuShareExecutor(BaseExecutor):
    def __init__(self, api_name: str='tushare', save_dir: str=None,*args, **kwargs):
        super().__init__(api_name, save_dir, *args, **kwargs)
        self.pro_api = ts.pro_api(token=TUSHARE_TOKEN, timeout=100)
        ts.set_token(TUSHARE_TOKEN)
        
    def get_stock_list(self, *args, **kwargs)->pd.DataFrame:
        """获取股票列表"""
        raise NotImplementedError
    
    def get_zs_realtime(self, *args, **kwargs)-> dict:
        """获取三大指数实时数据"""
        codes = kwargs.get('codes', ['000001.SH', '399001.SZ', '399006.SZ'])
        codes = ','.join(codes)
        df_data = ts.realtime_quote(ts_code=codes, src='sina')
        if df_data is None:
            return []
        df_data.DATE = df_data.DATE.apply(fmt_date)
        df_data.AMOUNT = df_data.AMOUNT.apply(scientific_number_convert)
        df_data['change'] = round((df_data.PRICE -df_data.PRE_CLOSE)*100/df_data.PRE_CLOSE, 2)
        dict_data = self.dftodict(df_data)
        return dict_data
    
    def get_real_time_data(self, *args, **kwargs):
        """获取实时数据"""
        return_list = kwargs.get('return_list', False) #直接返回实时数据list
        name_convert = kwargs.get('name_convert', True) #转换为中文名
        analyzer = kwargs.get('analyzer')
        params = kwargs.get('params')
        src = params.get('src', 'sina')
        ts_code = params.get('ts_code', [])
        if not isinstance(ts_code, list):
            ts_code = [ts_code]
        if len(ts_code)==0:
            if return_list:
                return []
            else:
                return {}
        codes = format_ts_code(ts_code)
        codes = self.group_codes(codes, 50)
        res = []
        for code_list in tqdm(codes):
            code_str = ','.join(code_list)
            # self.logger.info('get_real_time_data %s', code_str)
            df_data = ts.realtime_quote(ts_code=code_str, src=src)
            if df_data is None:
                return []
            df_data.rename(columns={k:k.lower() for k in df_data.columns.to_list()}, inplace=True)
            # if ABUPY:
            #     ABuSymbolPd.calc_atr(df_data)
            if df_data is None:
                continue
            dict_data = self.dftodict(df_data)
            res += dict_data
        res = self.filter_data(res)
        if return_list:
            return res
        if SAVE_DB:
            self.mysql_utils.insert_tushare_real_time_data_to_db(res)
        if SAVE_MOGODB:
            MongoDBUtil().insert_real_time_data(data=res)
        res = self.wrapper_res_use_wzw(res)
        res = self._item2dict(self._data_wrapper(res, TuShareRealTimeQuoteItem))
        if SAVE_JSON:
            save_json(res, os.path.join(self.save_dir, f"real_time_data_{self.request_count}.json"))
        analysis_res = self.analysis(analyzer=analyzer, infos=res)
        res = {'A股实时数据': res}
        res.update(analysis_res)
        if name_convert:
            res = self.type2str(res)
        return res
    
    def wrapper_res_use_wzw(self, infos:List[Dict]):
        """用wzw数据重新装饰并计算涨幅"""
        info_set = LoadJsonInfo()
        try:
            for info in infos:
                name = info.get('name')
                wrapper_dict = info_set.load_concept_from_wzw_data(name)
                info.update(wrapper_dict)
                if 'pre_close' in info.keys() and 'price' in info.keys():
                    increase = cal_increase(pre_close=info.get('pre_close',0), now_price=info.get('price', 0))
                    info.update({'zdfd': increase})
                high = info['high']
                low = info['low']
                pre_close = info['pre_close']
                zhfu = cal_amplitude(high=high, low=low, pre_close=pre_close)
                info['zhfu'] = zhfu
                info['hslv'] = cal_hslv(cjl=info['volume'], ltgb=info.get('ltgb', -1))
        except Exception as e:
            self.logger.error(f"{str(e)}, {str(info.get('ts_code'))}")
        return infos
    
    def get_day_k_line(self, *args, **kwargs):
        """获取日线数据"""
        params = kwargs.get('params')
        ts_code = params.get('ts_code', [])
        start_date = params.get('start_date').replace('-', '')
        end_date = params.get('end_date').replace('-', '')
        if not isinstance(ts_code, list):
            ts_code = [ts_code]
        codes = format_ts_code(ts_code)
        codes = self.group_codes(codes)
        res = []
        for code_list in tqdm(codes):
            code_str = ','.join(code_list)
            df_data = self.pro_api.daily(ts_code=code_str, start_date=start_date, end_date=end_date)
            dict_data = self.dftodict(df_data)
            if len(dict_data)>0:
                res += dict_data
        self.logger.info(f'pre filter: {len(res)}')
        res = self._item2dict(self._data_wrapper(res, TuShareDailyDataItem))
        res = self.filter_data(res)
        self.logger.info(f'dump {len(res)}!')
        if SAVE_JSON:
            save_json(res, os.path.join(self.save_dir, f"day_k_line_{start_date}-_{end_date}.json"))
        return res
    
    def dftodict(self, df:pd.DataFrame)->Dict:
        "df转dict"
        keys = [x.lower() for x in list(df.columns)]
        res = []
        for values in df.values:
            data  = dict(zip(keys, list(values)))
            res.append(data)
        
        return res

    


if __name__ == '__main__':
    res = TuShareExecutor().get_zs_realtime()
    print(res)
    