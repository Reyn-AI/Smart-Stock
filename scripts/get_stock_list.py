"""获取所有股票实时数据脚本"""
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from argparse import ArgumentParser
from src.utils.constant import WZW_COMMON_STOCK_LIST_API
from src.view.excel import WZWExcel
from src.utils.common import *
from src.api.wzw_executor import WZWExecutor
from src.engine.engine import Engine

class WZWDataScript:
    """歪枣网数据爬取工具"""

    def __init__(self):
        api = WZWExecutor()
        excel_path = os.path.join(
            api.save_dir, f'{get_time(template="%Y_%m_%d")}_股票列表.xlsx')
        self.viewer = WZWExcel(save_path=excel_path)
        self.engine = Engine(api=api, viewer=self.viewer)

    def get_stock_list(self, stock_type=[1]):
        """获取某板块股票列表
        """
        params = {
            "code": "all",
            "type": stock_type,
            "fields": "all",
        }
        config = WZW_COMMON_STOCK_LIST_API
        self.engine.run(api_type='stock_list',
                        config=config, params=params)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-type', help="资产类型，取值范围：1|沪深京A股；2|沪深京B股；3|港股；4|美股；5|黄金；6|汇率；7|Reits；10|沪深指数；11|香港指数；12|全球指数；13|债券指数；20|场内基金；30|沪深债券；40|行业板块；41|概念板块；42|地域板块",
        nargs='+',
        default=1)
    args = parser.parse_args()

    WZWDataScript().get_stock_list(stock_type=args.type)

