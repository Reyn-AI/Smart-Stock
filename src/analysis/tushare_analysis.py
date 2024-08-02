"""数据分析"""
from typing import List, Dict
import abc
import math
from .base import BaseAnalysis
from src.utils.common import *
import math
from copy import deepcopy
from src.utils.registy import analysis_register

@analysis_register(name='涨停股票', params=[])
class TuShareDataAnalysis(BaseAnalysis):
    """涨停股票分析"""

    async def analysis(self, infos: List[Dict]):
        """获取涨停的股票"""
        infos = super().analysis(infos=infos, pd2dict=True)
        zt_stocks = []
        for info in infos:
            if 'price' in info.keys() and 'open' in info.keys():
                now_price = info.get('price', 0)
                pre_close = info.get('pre_close', 0)
                increase = cal_increase(pre_close=pre_close, now_price=now_price)
                if math.ceil(increase)>=10:
                    zt_stocks.append(info)
        res = {"今日涨停股票": zt_stocks}
        if self.kwargs.get('plot'):
            res['plot'] = deepcopy(zt_stocks)
        return res
    
@analysis_register(name='涨幅大于百分之n股票', params=[{'code':'threshold', 'name':"涨幅大于n", 'default':5, 'uiType':'input'}])
class TuShareDataAnalysisZFltn(BaseAnalysis):
    """TuShare涨幅大于百分之n股票"""

    async def analysis(self, infos: List[Dict], **kwargs):
        """获取涨幅大于n的股票"""
        infos = super().analysis(infos=infos, pd2dict=True)
        threshold = self.kwargs.get('threshold', 5)
        res_stocks = []
        for info in infos:
            if 'price' in info.keys() and 'open' in info.keys():
                now_price = info.get('price', 0)
                pre_close = info.get('pre_close', 0)
                increase = cal_increase(pre_close=pre_close, now_price=now_price)
                if increase >= threshold:
                    res_stocks.append(info)
        res = {f"涨幅大于{threshold}%的股票": res_stocks}
        return res
    
@analysis_register(name='今日开盘价大于等于n%*昨日收盘价', params=[{'code':'n', 'name':"n", 'default':0.97, 'uiType':'input'}])
class TuShareDataAnalysisPriceltyestday(BaseAnalysis):
    """TuShare数据今日开盘价大于等于n%*昨日收盘价的股票且当前价格大于昨收"""

    async def analysis(self, infos: List[Dict]):
        """TuShare数据今日开盘价大于等于n%*昨日收盘价的股票"""
        infos = super().analysis(infos=infos, pd2dict=True)
        n = self.kwargs.get('n', 0.97)
        res_stocks = []
        for info in infos:
                if 'open' in info.keys() and 'pre_close' in info.keys():
                    if float(info.get('open', 0))>n*float(info.get('pre_close', math.nan)) and float(info.get('price'))> float(info.get('pre_close')):
                        res_stocks.append(info)
        res = {f"今日开盘大于昨日收盘{n*100}%的股票": res_stocks}
        return res
    
@analysis_register(name='今日收盘价大于等于最高价的股票', params=[])
class TuShareDataAnalysisPriceltmean(BaseAnalysis):
    """TuShare数据今日收盘价大于等于最高价的股票"""

    async def analysis(self, infos: List[Dict]):
        """TuShare数据今日收盘价大于等于最高价的股票"""
        infos = super().analysis(infos=infos, pd2dict=True)
        res_stocks = []
        for info in infos:
            if 'price' in info.keys() and 'high' in info.keys():
                if float(info.get('price', 0))>=float(info.get('high', math.nan)):
                    res_stocks.append(info)
        res = {"收盘价大于等于最高价的股票": res_stocks}
        return res
    
@analysis_register(name='最低价格比开盘价高的股票',params=[])
class TuShareDataAnalysisLowltOpen(BaseAnalysis):
    """最低价格比开盘价高"""
    async def analysis(self, infos: List[Dict]):
        """TuShare数据今日收盘价大于等于最高价的股票"""
        infos = super().analysis(infos=infos, pd2dict=True)
        res_stocks = []
        for info in infos:
            if 'low' in info.keys() and 'open' in info.keys():
                if float(info.get('low', 0))>=float(info.get('open', math.nan)):
                    res_stocks.append(info)
        res = {"最低价比开盘价高": res_stocks}
        return res
    
@analysis_register(name='最低价格比开盘价高,当前价格是最高价', params=[])
class TuShareDataAnalysisLowltOpenAndHight(BaseAnalysis):
    """最低价格比开盘价高,当前价格是最高价"""
    async def analysis(self, infos: List[Dict]):
        """最低价格比开盘价高,当前价格是最高价"""
        infos = super().analysis(infos=infos, pd2dict=True)
        res_stocks = []
        for info in infos:
            if 'low' in info.keys() and 'open' in info.keys():
                if float(info.get('low', 0))>=float(info.get('open', math.nan)) and float(info.get('price', 0))>=float(info.get('high', math.nan)):
                    res_stocks.append(info)
        res = {"最低价比开盘价高且上升": res_stocks}
        return res
    
@analysis_register(name='当前价格比均价高的股票', params=[])
class TuShareDataAnalysisLowltMean(BaseAnalysis):
    """收于均线上"""
    async def analysis(self, infos: List[Dict]):
        infos = super().analysis(infos=infos, pd2dict=True)
        res_stocks = []
        for info in infos:
            if 'low' in info.keys() and 'open' in info.keys():
                mean = (info['low'] + info['high'])/2
                if float(info.get('price', 0))>=mean and float(info.get('price', 0)) > float(info.get('pre_close', 0)) \
                   and abs(float(info.get('price', 0))-float(info.get('high', 0)))/float(info.get('high', 1))<0.01:
                    res_stocks.append(info)
        res = {"收于均线上": res_stocks}
        if self.kwargs.get('plot'):
            res['plot'] = deepcopy(res_stocks)
        return res
    
# @analysis_register(name='根据角度策略选股', params=[{'code':'threshold_ang_min', 'name':"最小角度", 'default':10, 'uiType':'input'},
#                                             {'code':'threshold_ang_max', 'name':"最大角度", 'default':50, 'uiType':'input'}])
# class TuShareDataAnalysisSelectByAngle(BaseAnalysis):
#     """根据角度策略选股"""
#     async def analysis(self, infos: List[Dict]):
#         """根据角度策略选股"""
#         infos = super().analysis(infos=infos, pd2dict=True)
#         threshold_ang_min = self.kwargs.get('threshold_ang_min', 0) #最小角度
#         threshold_ang_max = self.kwargs.get('threshold_ang_max', 90) #组大角度
#         n_folds = self.kwargs.get('n_folds', 1) #决策周期
#         sympols = [x.get('ts_code')or x.get('code') for x in infos]
#         choice_sympols = SelectStock(n_folds=n_folds,
#                                      threshold_ang_max = threshold_ang_max,
#                                      threshold_ang_min = threshold_ang_min,
#                                      show=self.kwargs.get('show')).select(sympols)
#         choice_sympols = [abu_code_to_code(x) for x in choice_sympols]
#         res_stocks = []
#         for info in infos:
#             if abu_code_to_code(info.get('ts_code')or info.get('code')) in choice_sympols:
#                 res_stocks.append(info)
#         res = {f"近{n_folds}年k线角度>{threshold_ang_min}": res_stocks}
#         if self.kwargs.get('plot'):
#             res = {"plot": deepcopy(res_stocks)}
#         return res