"""tusharek线数据爬取脚本"""
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from argparse import ArgumentParser

from src.utils.common import load_json
from src.engine.engine import Engine
from src.api.tushare_executor import TuShareExecutor
from src.utils.common import *

class TuShareCrawl:
    """Tushare数据爬取工具"""

    def __init__(self):
        self.engine = Engine(api=TuShareExecutor())

    def get_k_min_data(self, json_path, s_date, e_date, length=-1):
        """获取某时间范围内的分钟数据
            date_formate: yyyy-MM-dd HH:mm:ss
        """
        raise NotImplementedError()

    def get_hour_data(self, json_path, s_date, e_date, length=-1):
        """获取某时间范围内的小时线数据
            date_formate: yyyy-MM-dd HH:mm:ss
        """
        raise NotImplementedError
    
    def get_day_data(self, json_path, s_date, e_date, length=-1):
        """获取某时间范围内的日线数据
            date_formate: yyyy-MM-dd HH:mm:ss
        """
        if json_path.endswith('json'):
            codes = self.load_stock_codes(json_path=json_path, length=length)
        else:
            codes = [json_path] #传入的是代码
        params = {
            'start_date': s_date,
            'end_date': e_date,
            'ts_code':codes
        }
        return self.engine.run(api_type='day_k_line', params=params)


    def load_stock_codes(self, json_path, length=-1):
        """从json加载股票代码"""
        data = load_json(json_path)
        data = list(data.keys())
        # data = list(filter(lambda x:x.startswith(('00', '60')), data))
        return data[:length]


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s_date', help="开始日期, 格式:yyyy-MM-dd, 如2024-03-01")
    parser.add_argument('-e_date', help='结束日期')
    parser.add_argument('-json', help='codes json文件路径')
    parser.add_argument('-length', help='爬取的股票数量', type=int, default=-1)
    parser.add_argument('-k_type', help='K线类型', choices=['min', 'day', 'hour'], default='day')
    args = parser.parse_args()

    if args.k_type == 'min':
        TuShareCrawl().get_k_min_data(json_path=args.json, s_date=args.s_date,
                                  e_date=args.e_date,
                                  length=args.length)
    if args.k_type == 'day':
        TuShareCrawl().get_day_data(json_path=args.json, s_date=args.s_date,
                                  e_date=args.e_date,
                                  length=args.length)
    if args.k_type == 'houur':
        TuShareCrawl().get_hour_data(json_path=args.json, s_date=args.s_date,
                                  e_date=args.e_date,
                                  length=args.length)
        
    