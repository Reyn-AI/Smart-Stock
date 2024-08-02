"""获取所有股票实时数据脚本"""
from typing import List
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from argparse import ArgumentParser
from src.view.excel import AkShareExcel
from src.utils.common import *
from src.api.akshare_executor import AkShareExecutor
from src.engine.engine import Engine
from src.analysis.akshare_analysis import *
from src.view.mpf_plot import MpfPlot
from src.items.enum_item import ApiType

class AkShareDataScript:
    """AkShare数据爬取工具"""

    def __init__(self):
        self.api = AkShareExecutor()

    def get_k_min_data(self, codes:List):
        """获取主板当天分钟数据
        """
        excel_path = os.path.join(
        self.api.save_dir, f'{get_time(template="%Y_%m_%d")}_akshare股票数据.xlsx')
        self.viewer = AkShareExcel(save_path=excel_path)
        self.engine = Engine(api=self.api, viewers=[self.viewer])
        analyzer = [KHistoryAnalysis(filter_zb=True)
                    ]
        self.engine.run(api_type='minute_k_line', codes=codes, analyzer=analyzer)

    def get_ths_special_data(self, how='cxg'):
        excel_path = os.path.join(
        self.api.save_dir, f'{get_time(template="%Y_%m_%d")}_同花顺特色股票数据.xlsx')
        self.viewer = AkShareExcel(save_path=excel_path)
        self.engine = Engine(api=self.api, viewers=[self.viewer])
        self.engine.run(api_type='ths_special_data', how=how) #获取同花顺特色数据
    
    def get_history_real_time_data(self, codes:List):
        viewer = MpfPlot()
        self.engine = Engine(api=self.api, viewers=[viewer])
        self.engine.run(api_type='history_real_time_data', codes=codes, exec_type=ApiType.AKSHARE) #获取同花顺特色数据


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-codes', nargs='+')
    parser.add_argument('-t', default='k_min')
    parser.add_argument('-how', default='all')
    args = parser.parse_args()

    if args.codes and args.codes[0].endswith('.json'):
        codes = load_json(args.codes[0])
        codes = list(codes.keys())
    else:
        codes = args.codes
    if args.t == 'k_min':
        AkShareDataScript().get_k_min_data(codes=args.codes)
    elif args.t == 'ths':
        AkShareDataScript().get_ths_special_data(how=args.how)
    elif args.t =='rt':
        AkShareDataScript().get_history_real_time_data(codes=args.codes)
