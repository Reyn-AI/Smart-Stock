"""数据加载器"""
from typing import List
import pandas as pd
import datetime
from tqdm import tqdm
from src.utils.common import format_ts_code
from src.engine import Engine
from src.api import TuShareExecutor
from src.utils.common import *

class JsonDataLoader:
    
    def __init__(self, 
                 json_path:str=None,
                 ):
        self.json_path = json_path
        if json_path:
            self.__pre_loader()
        
    def __pre_loader(self):
        """预先读取文件"""
        self.daily_price = pd.read_json(self.json_path)
        self.daily_price['trade_date'] = pd.to_datetime(self.daily_price['trade_date'], format='%Y%m%d')
    
    def load_from_web(self, codes:List, s_date, e_date):
        res = self.get_day_data(codes=codes, s_date=s_date, e_date=e_date)
        df = tushare_dict_to_df(res)
        df = df.rename(columns={'trade_date':'ds', 'close':'y', 'ts_code':'unique_id'}) #Index(['unique_id', 'ds', 'open', 'high', 'low', 'y', 'pre_close', 'change','pct_chg', 'vol', 'amount'],
        return df
    
    def get_day_data(self, codes, s_date, e_date):
        """获取某时间范围内的日线数据
            date_formate: yyyy-MM-dd HH:mm:ss
        """
        self.engine = Engine(api=TuShareExecutor())
        params = {
            'start_date': s_date,
            'end_date': e_date,
            'ts_code': codes
        }
        return self.engine.run(api_type='day_k_line', params=params)
    
    def load(self):
        """加载tushare格式json数据"""
        self.daily_price = self.daily_price.rename(columns={'trade_date':'ds', 'close':'y', 'ts_code':'unique_id'})
        return self.daily_price
    
    # print("All stock Done !")


if __name__ == '__main__':
    aa = JsonDataLoader('/data/application/lqy/codes/gitee/smart-stock/src/models/day_k_line_20210101-_20240403.json').load_from_web(codes=['600640'], s_date='2023-01-01', e_date='2024-04-07')
    breakpoint()