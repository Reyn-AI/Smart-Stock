"""数据分析"""
from typing import List, Dict, Union
import abc
import math
import pandas as pd
from src.utils.common import *
from src.analysis.data_analysis import BaseAnalysis
from src.api.tushare_executor import TuShareExecutor
from src.utils.registy import analysis_register, analysis_register_history


class KminVWAPAnalysis(BaseAnalysis):
    """根据分钟k线vwap选股"""
    
    def analysis(self, infos:pd.DataFrame):
        ts_codes = infos.ts_code.drop_duplicates().to_list()
        res = []
        for code in ts_codes:
            code_data = infos.query(f'ts_code=="{code}"')
            vwap = cal_vwap(code_data)
            if len(code_data[code_data.close>vwap]) >= 2/3*len(code_data):
                res.append(code_data)
        res = dftodict(pd.concat(res))        
        return {'分钟线>2/3 vmap':res}                

class KHistoryAnalysis(BaseAnalysis):
    """股价一直在均线上"""
    def analysis(self, infos:pd.DataFrame):
        ts_codes = infos.ts_code.drop_duplicates().to_list()
        res = []
        for code in ts_codes:
            code_data = infos.query(f'ts_code=="{code}"')
            df = cal_k_mean(code_data)
            if len(df[df.close>=code_data['mean']]) > 2/3*len(code_data):
                res.append(code)
        #获取相关代码数据
        res = TuShareExecutor().get_real_time_data(params={'ts_code':res})
        res['分钟线三分之二时间位于均线上'] = res.pop('A股实时数据')   
        return res

@analysis_register_history(name='同花顺特色股票', params=[{'code':'how', 'name':"类型", 'default':['cxg'],
                                            'uiType':'select',
                                            'selectChoices':[{'code':'cxg', 'name':'创新高'},
                                                               {'code':'cxd', 'name':'创新低'},
                                                               {'code':'lxsz', 'name':'连续上涨'},
                                                               {'code':'lxxd', 'name':'连续下跌'},
                                                               {'code':'cxfl', 'name':'持续放量'},
                                                               {'code':'cxsl', 'name':'持续缩量'},
                                                               {'code':'xstp', 'name':'向上突破'},
                                                               {'code':'xxtp', 'name':'向下突破'},
                                                               {'code':'ljqs', 'name':'量价齐升'},
                                                               {'code':'ljqd', 'name':'量价齐跌'},
                                                               {'code':'xzjp', 'name':'验资举牌'}]}])
class AkShareThsSpecialStocks(BaseAnalysis):
    """最低价格比开盘价高"""
    def __init__(self, *args, **kwargs):
        self.how = kwargs.get('how', ['cxg'])
    async def analysis(self, infos: List[Dict], **kwargs):
        """TuShare数据今日收盘价大于等于最高价的股票"""
        from src.engine.engine import Engine
        from src.api.akshare_executor import AkShareExecutor
        engine_akshare = Engine(api=AkShareExecutor())
        res_ths = engine_akshare.run(api_type='ths_special_data', how=self.how) #获取同花顺特色数据
        return res_ths