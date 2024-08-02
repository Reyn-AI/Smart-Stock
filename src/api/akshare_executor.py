from typing import List, Dict
import akshare as ak
from src.api.base import BaseExecutor
from src.utils.common import *
from src.utils.parallel_util import *
from src.crawls.sina_crawl import *
import akshare as ak
import pandas as pd
from tqdm import tqdm
import numpy as np

class AkShareExecutor(BaseExecutor):
    
    def __init__(self, api_name: str='AkShare', save_dir: str = None, *args, **kwargs):
        super().__init__(api_name, save_dir, *args, **kwargs)
    
    def get_history_real_time_data(self, *args, **kwargs):
        """获取分线数据"""
        codes = kwargs.get('codes')
        if not isinstance(codes, list):
            codes = [codes]
            # codes = list(set(codes) & set(self.all_codes)) #过滤不存在的代码
        filter_zb = kwargs.get('filter_zb', True) #只保留主板数据
        if filter_zb:
            codes = self.filter_codes_zb(codes)
        n_jobs = kwargs.get('n_jobs', max(1, int(len(codes) // 100))) #并行数量,默认每个进程100个任务
        codes_set = self.group_codes(codes=codes, number=n_jobs)
        res = Parallel(n_jobs=n_jobs)(delayed(self._parallel_get)(func=self._get_hisory_real_time_data, codes=codes) for codes in codes_set)
        res = pd.concat(res, axis=0)
        res.set_index(np.arange(len(res)), inplace=True)
        analyzer = kwargs.get('analyzer')
        if analyzer:
            res = self.analysis(analyzer=analyzer, infos=res)
        return res
    
    def get_minute_k_line(self, *args, **kwargs):
        """获取当日分钟不复权数据"""
        codes = kwargs.get('codes')
        if not isinstance(codes, list):
            codes = [codes]
            # codes = list(set(codes) & set(self.all_codes)) #过滤不存在的代码
        filter_zb = kwargs.get('filter_zb', True) #只保留主板数据
        if filter_zb:
            codes = self.filter_codes_zb(codes)
        n_jobs = kwargs.get('n_jobs', max(1, int(len(codes) // 100))) #并行数量,默认每个进程100个任务
        codes_set = self.group_codes(codes=codes, number=n_jobs)
        res = Parallel(n_jobs=n_jobs)(delayed(self._parallel_get)(func=self._get_minute_k_line, codes=codes) for codes in codes_set)
        res = pd.concat(res, axis=0)
        res.set_index(np.arange(len(res)), inplace=True)
        analyzer = kwargs.get('analyzer')
        if analyzer:
            res = self.analysis(analyzer=analyzer, infos=res)
        return res
    
    def get_ths_special_data(self, *args, **kwargs):
        """获取同花顺特色数据"""
        how_list = kwargs.get('how', ['all'])
        if isinstance(how_list, str):
            how_list = [how_list]
        all_res = {}
        for how in how_list:
            if how == 'all' or how=='cxg':
                cxg = ak.stock_rank_cxg_ths().fillna(-1) #创新高
                all_res['创新高'] =  dftodict(cxg)
            if how == 'all' or how=='cxd':
                cxd = ak.stock_rank_cxd_ths().fillna(-1) #创新低
                all_res['创新低'] = dftodict(cxd)
            if how == 'all' or how=='lxsz':
                lxsz = ak.stock_rank_lxsz_ths().fillna(-1) #连续上涨
                all_res['连续上涨'] = dftodict(lxsz)
            if how == 'all' or how=='lxxd':
                lxxd = ak.stock_rank_lxxd_ths().fillna(-1) #连续下跌
                all_res['连续下跌'] = dftodict(lxxd)
            if how == 'all' or how=='cxfl':
                cxfl = ak.stock_rank_cxfl_ths().fillna(-1) #持续放量
                all_res['持续放量'] = dftodict(cxfl)
            if how == 'all' or how=='cxsl':
                cxsl = ak.stock_rank_cxsl_ths().fillna(-1) #持续缩量
                all_res['持续缩量'] = dftodict(cxsl)
            if how == 'all' or how=='xstp':
                xstp = ak.stock_rank_xstp_ths().fillna(-1) #向上突破
                all_res['向上突破'] =dftodict(xstp)
            if how == 'all' or how=='xxtp':
                xxtp = ak.stock_rank_xxtp_ths().fillna(-1) #向下突破
                all_res['向下突破'] = dftodict(xxtp)
            if how == 'all' or how=='ljqd':
                ljqd = ak.stock_rank_ljqd_ths().fillna(-1) #量价齐跌
                all_res['量价齐跌'] = dftodict(ljqd)
            if how == 'all' or how=='ljqs':
                ljqs = ak.stock_rank_ljqs_ths().fillna(-1) #量价齐升
                all_res['量价齐升'] = dftodict(ljqs)
            if how == 'all' or how=='xzjp':
                xzjp = ak.stock_rank_xzjp_ths().fillna(-1) #险资举牌
                all_res['验资举牌'] = dftodict(xzjp)
            if how =='all':
                break
        return all_res
    
    def _parallel_get(self, func, codes):
        """并行执行"""
        res = []
        for code in tqdm(codes):
            df = func(code)
            df['ts_code'] = code
            res.append(df)
        return pd.concat(res, axis=0)
    
    def _get_minute_k_line(self, code, **kwargs):
        """获取当日分线数据"""
        code = code_to_abu_code(code)
        df = stock_zh_a_minute(symbol=code)
        return df
    
    def _get_hisory_real_time_data(self, code, **kwargs):
        """获取当日实时历史数据"""
        code = code_to_abu_code(code)
        df = ak.stock_zh_a_tick_tx_js(code)
        return df
    
    def get_real_time_data(self, *args, **kwargs):
        """获取沪深京A股实时数据"""
        analyzer = kwargs.get('analyzer')
        return_list = kwargs.get('return_list', True)
        codes = kwargs.get('codes')
        df = ak.stock_zh_a_spot_em()
        df.rename(columns={'代码':'code',
                           '名称':'name',
                           '最新价':'price',
                           '涨跌幅':'change',
                           '成交量':'volume',
                           '成交额':'amount',
                           '今开':'open',
                           '昨收':'pre_close',
                           '最高':'high',
                           '最低':'low'}, inplace=True)
        df = df.drop('序号', axis=1)
        df = df[df.volume>0]
        df['volume'] = df['volume'].apply(scientific_number_convert)
        df['amount'] = df['amount'].apply(scientific_number_convert)
        df = df.fillna(-1)
        res = dftodict(df)
        if return_list:
            return res
        analysis_res = self.analysis(analyzer=analyzer, infos=res)
        res = self.wrapper_res_use_wzw(res)
        res = {'A股实时数据': res}
        res.update(analysis_res)
        res = self.type2str(res)
        return res


if __name__ == '__main__':
    res = AkShareExecutor().get_minute_k_line(codes=['600640', '600641'])
    breakpoint()