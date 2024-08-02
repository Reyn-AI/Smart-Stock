"""获取所有股票实时数据脚本"""
from typing import List
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from argparse import ArgumentParser
from src.view.excel import TuShareExcel
from src.utils.common import *
from src.api.tushare_executor import TuShareExecutor
from src.engine.engine import Engine
from src.analysis.tushare_analysis import *
from src.view.abu_plot import LineViewer

class TuShareDataScript:
    """歪枣网数据爬取工具"""

    def __init__(self):
        api = TuShareExecutor()
        excel_path = os.path.join(
            api.save_dir, f'{get_time(template="%Y_%m_%d")}_实时股票数据.xlsx')
        self.viewer = TuShareExcel(save_path=excel_path)
        # self.viewer_plot = LineViewer(how='all')
        self.engine = Engine(api=api, viewers=[self.viewer])

    def get_real_time_data(self, codes:List):
        """获取主板实时数据
            date_formate: yyyy-MM-dd HH:mm:ss
        """
        params = {
            "ts_code": codes,
            "src": 'sina',
        }
        analyzer = [TuShareDataAnalysis(plot=True),
                    TuShareDataAnalysisZFltn(threshold=3),
                    TuShareDataAnalysisPriceltyestday(n=0.99),
                    TuShareDataAnalysisLowltOpenAndHight(),
                    TuShareDataAnalysisLowltMean(),
                    # TuShareDataAnalysisSelectByAngle(threshold_ang_min=15,n_folds=1, show=True, plot=False)
                    ]
        self.engine.run(api_type='real_time_data', params=params, analyzer=analyzer)




if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-codes', nargs='+')
    args = parser.parse_args()

    if args.codes[0].endswith('.json'):
        codes = load_json(args.codes[0])
        codes = list(codes.keys())
    else:
        codes = args.codes   
    TuShareDataScript().get_real_time_data(codes=codes)

