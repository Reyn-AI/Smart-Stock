from typing import List, Dict
from src.utils.common import *
from src.utils.stock_utils import *
from src.api.easyquotation_executor import EasyQuotationExecutor
from .base import HistoryBaseAnalysis, BaseAnalysis
from src.utils.registy import analysis_register_history, analysis_register
from src.backtest.strategys.factors import *
from concurrent.futures import ThreadPoolExecutor
from src.utils.constant import BAO_STOCK_NAME
import qstock  as qs
import asyncio
from src.utils.parallel_util import Parallel,delayed

def static_open_data(infos: List, open_key="open", pre_close_key='pre_close', code_key='ts_code'):
    """统计开盘情况"""
    res_stocks = {'大于昨日收盘价的股票': [],
             '高开3个点以上的股票':[],
             '一字涨停的股票': [],
             '大于昨日收盘价99%的股票':[],
             '一字跌停的股票':[],
             '低开3个点以下的股票':[]}
    if infos is None or len(infos)==0:
        return res_stocks
    for info in infos:
        if open_key in info.keys() and pre_close_key in info.keys():
            open = info[open_key]
            code = info.get(code_key) or info.get('code')
            pre_close = info[pre_close_key]
            if open>pre_close:
                res_stocks['大于昨日收盘价的股票'].append(info)
            if open>=(1 + 3/100) * pre_close:
                res_stocks['高开3个点以上的股票'].append(info)
            if open>=(1 + 10/100) * pre_close and code.startswith(('60', '0')):
                res_stocks['一字涨停的股票'].append(info)
            if open>=(1 + 20/100) * pre_close and code.startswith(('68', '30', '8')):
                res_stocks['一字涨停的股票'].append(info)
            if open>=(1 - 1/100) * pre_close:
                res_stocks['大于昨日收盘价99%的股票'].append(info)
            if open - (1 - 10/100) * pre_close<=1e-5 and code.startswith(('60', '0')):
                res_stocks['一字跌停的股票'].append(info)
            if open - (1 - 20/100) * pre_close<=1e-5 and code.startswith(('68', '30', '8')):
                res_stocks['一字跌停的股票'].append(info)
            if open - (1 - 3/100) * pre_close<=1e-5:
                res_stocks['低开3个点以下的股票'].append(info)
    return res_stocks


def merge_real_time_data(code, n =30, frequency='d'):
    """讲历史数据与最新数据整合
        Args:
            n 历史时间窗口长度
            frequency k线频率
    """
    dates = get_time_before_n(n=n)
    e_date = dates[0]
    s_date = dates[-1]
    history_k_line = get_day_k_data(code=code, start_date=s_date, end_date=e_date, api_type='baostock', frequency=frequency)
    now_data = EasyQuotationExecutor().get_realtime_data_by_code(code=code)
    date = now_data[list(now_data.keys())[0]]['datetime'].strftime('%Y-%m-%d %H:%M:%S')
    open = now_data[list(now_data.keys())[0]]['open']
    high = now_data[list(now_data.keys())[0]]['high']
    low = now_data[list(now_data.keys())[0]]['low']
    close = now_data[list(now_data.keys())[0]]['close']
    volume = now_data[list(now_data.keys())[0]]['volume']
    date_df = pd.DataFrame({'date':[date], 'time':[date], 'code':[code], 'open':[open],'high':[high], 'low':[low], 'close':[close], 'volume':[volume]})
    new_k_line = pd.concat([history_k_line, date_df])
    return new_k_line

def merge_real_time_data(code, metric_list:List[Dict], n =30, frequency='d'):
    data = merge_real_time_data(code=code, n=n, frequency=frequency)


@analysis_register_history(name='RSRS因子选股', params=[{'code':'N', 'name':"窗口长度(天)", 'default':16, 'uiType':'input'},
                                            {'code':'threshold', 'name':"阈值", 'default':0.7, 'uiType':'input'},
                                            {'name':'观察期时间窗口M','code':'M', 'default':300, 'desc':'RSRS观察期时间窗口长度', 'uiType':'input'},
                                            {'name':'k线类型', 'code':'frequency', 'default':'d', 'uiType':'selectDate'},
                                            {'code':'startDate', 'name':'开始日期', 'uiType':'date', 'default':''},
                                             {'code':'endDate', 'name':'结束日期', 'uiType':'date', 'default':''}])
class RSRSDataAnalysisSelect(BaseAnalysis):
    """根据承压线选股"""
    
    async def analysis(self, *args, **kwargs):
        all_codes = get_all_stock_codes(market=self.market)
        try:
            codes = group_codes(all_codes)
            results_list = await asyncio.gather(*[self.single_analysis_multi(codes=x, start_date=self.startDate, end_date=self.endDate, frequency=self.frequency) for x in codes])
            results = [x for y in results_list for x in y]
            return results
        except Exception as e:
            self.logger.error("RSRSDataAnalysisSelect:"+str(e))
    
    async def single_analysis_multi(self, codes:list, start_date, end_date, frequency):
        res_codes = []
        df_list = get_day_k_data_multi(codes=codes,
                                    start_date=start_date,
                                    end_date=end_date,
                                    frequency=frequency,
                                    return_list=True,
                                    api_type='qstock')
        if df_list is None or len(df_list)==0:
            return res_codes
        # rsrs_list = await asyncio.gather(*[RSRS().async_call_metric(df['high'], df['low'], N=int(self.N), M=int(self.M)) for df in df_list])
        rsrs_list = Parallel(n_jobs=20, backend='process')([delayed(RSRS().call_metric)(df['high'], df['low'], N=self.N, M=self.M, src=df) for df in df_list])
        for rsrs, df in rsrs_list:
            if rsrs[-1]>float(self.threshold):
                data = df.iloc[-1].to_dict()
                TUSHARE_TYPE_NAME.update(BAO_STOCK_NAME)
                data = type2str(data, type_str_dict=TUSHARE_TYPE_NAME)
                if len(rsrs)>3:
                    data[f'前天RSRS值'] = str(round(rsrs[-3], 3))
                    data[f'昨天RSRS值'] = str(round(rsrs[-2], 3))
                if len(rsrs)>7:
                    data[f'7天平均RSRS值'] = str(round(sum(rsrs[-7:])/7,3))
                data[f'RSRS值'] = str(round(rsrs[-1], 3))
                res_codes.append(data)
                # print(f'RSRSDataAnalysisSelect: {df.iloc[0]["name"]}, {rsrs[-1]}')
        return res_codes
        

    def single_analysis(self, code, start_date, end_date, frequency):
        res_codes = []
        df = get_day_k_data(code=code,
                                    start_date=start_date,
                                    end_date=end_date,
                                    frequency=frequency,
                                    api_type='abu' if frequency=='d' else 'qstock')
        if df is None or len(df)==0:
            return res_codes
        rsrs = RSRS()(df['high'], df['low'], N=int(self.N), M=int(self.M))
        if rsrs[-1]>float(self.threshold):
            data = df.iloc[-1].to_dict()
            TUSHARE_TYPE_NAME.update(BAO_STOCK_NAME)
            data = type2str(data, type_str_dict=TUSHARE_TYPE_NAME)
            name = LoadJsonInfo().get_name_by_code(code)
            if name is not None:
                data['股票名字'] = name
            data[f'RSRS值'] = rsrs[-1]
            res_codes.append(data)
            # self.logger.info(f'RSRSDataAnalysisSelect: {code}, {rsrs[-1]}')
        return res_codes
    
@analysis_register_history(name='实时交易盘口异动数据', params=[{'code':'how', 'name':"类型", 'default':['火箭发射'],
                                            'uiType':'select',
                                            'selectChoices':[{'code':'火箭发射', 'name':'火箭发射'},
                                                               {'code':'快速反弹', 'name':'快速反弹'},
                                                               {'code':'加速下跌', 'name':'加速下跌'},
                                                               {'code':'高台跳水', 'name':'高台跳水'},
                                                               {'code':'大笔买入', 'name':'大笔买入'},
                                                               {'code':'大笔卖出', 'name':'大笔卖出'},
                                                               {'code':'封涨停板', 'name':'封涨停板'},
                                                               {'code':'封跌停板', 'name':'封跌停板'},
                                                               {'code':'打开跌停板', 'name':'打开跌停板'},
                                                               {'code':'打开涨停板', 'name':'打开涨停板'},
                                                               {'code':'有大买盘', 'name':'有大买盘'},
                                                               {'code':'有大卖盘', 'name':'有大卖盘'},
                                                               {'code':'竞价上涨', 'name':'竞价上涨'},
                                                               {'code':'竞价下跌', 'name':'竞价下跌'},
                                                               {'code':'高开5日线', 'name':'高开5日线'},
                                                               {'code':'低开5日线', 'name':'低开5日线'},
                                                               {'code':'向上缺口', 'name':'向上缺口'},
                                                               {'code':'向下缺口', 'name':'向下缺口'},
                                                               {'code':'60日新高', 'name':'60日新高'},
                                                               {'code':'60日新低', 'name':'60日新低'},
                                                               {'code':'60日大幅上涨', 'name':'60日大幅上涨'},
                                                               {'code':'60日大幅下跌', 'name':'60日大幅下跌'}]}])
class ThsRealTimeChangeAnalysis(BaseAnalysis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_key = '代码'
        
    async def analysis(self, *args, **kwargs):
        """TuShare数据今日收盘价大于等于最高价的股票"""
        results = await asyncio.gather(*[self.get_data(how=x) for x in self.how])
        final_res = {}
        for how, result in results:
            res = super().analysis(result, pd2dict=True) #按市场过滤
            final_res[how] = res
        return final_res
    
    async def get_data(self, how):
        return how, qs.realtime_change(how)

if __name__ == '__main__':
    merge_real_time_data('600649', [], frequency='60')