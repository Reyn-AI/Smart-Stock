"""数据分析"""
from typing import List, Dict, Union
import abc
import math
import pandas as pd
from src.utils.common import dftodict
from .base import BaseAnalysis

class WZWDataAnalysis(BaseAnalysis):
    """涨停股票分析"""

    def analysis(self, infos: List[Dict]):
        """获取涨停的股票"""
        zt_stocks = []
        yestday_stocks = []
        for info in infos:
            if 'price' in info.keys() and 'ztj' in info.keys():
                if info.get('price') == info.get('ztj'):
                    zt_stocks.append(info)
                if '涨停' in info.get('z53'):
                    yestday_stocks.append(info)
        res = {"今日涨停股票": zt_stocks,
               "昨日涨停股票": yestday_stocks}
        return res

class WZWDataAnalysisZFltn(BaseAnalysis):
    """歪枣网涨幅大于百分之n股票"""

    def analysis(self, infos: List[Dict], **kwargs):
        """获取涨幅大于n的股票"""
        threshold = self.kwargs.get('threshold', 5)
        res_stocks = []
        for info in infos:
            if 'zdfd' in info.keys():
                if float(info.get('zdfd', 0))>threshold:
                    res_stocks.append(info)
        res = {f"涨幅大于百分之{threshold}的股票": res_stocks}
        return res

class WZWDataAnalysisPriceltyestday(BaseAnalysis):
    """歪枣网数据今日开盘价大于等于n%*昨日收盘价的股票"""

    def analysis(self, infos: List[Dict]):
        """歪枣网数据今日开盘价大于等于n%*昨日收盘价的股票"""
        n = self.kwargs.get('n', 0.97)
        res_stocks = []
        for info in infos:
            if 'open' in info.keys() and 'zrspj' in info.keys():
                if float(info.get('open', 0))>=n*float(info.get('zrspj', math.nan)) and float(info.get('price')>info.get('open')):
                    res_stocks.append(info)
        res = {f"今日开盘大于昨日收盘百分之{n*100}的股票": res_stocks}
        return res

class WZWDataAnalysisPriceltmean(BaseAnalysis):
    """歪枣网数据今日收盘价大于均价的股票"""

    def analysis(self, infos: List[Dict]):
        """歪枣网数据今日收盘价大于均价的股票"""
        res_stocks = []
        for info in infos:
            if 'jjia' in info.keys() and 'price' in info.keys():
                if float(info.get('price', 0))>float(info.get('jjia', math.nan)):
                    res_stocks.append(info)
        res = {"收盘价大于均价的股票": res_stocks}
        return res
