from src.utils.registy import factor_register 
from src.backtest.strategys import BaseFactor
from src.utils.stock_utils import *
import backtrader as bt

class ZtAndBackMAFactor(bt.Indicator):
    lines = ('zt_and_back_ma',)
    params = (('windows', 16),) #N:窗口长度， ma 均线类型

    def __init__(self):
        self.df = cal_exist_zt_in_windows(self.data._dataname, windows=self.p.windows).exist_zt.to_list() #self.data._dataname是原始DataFrame类型数据
        self.idx = 0
        
    def next(self):
       y = self.df[self.idx]
       self.l.zt_and_back_ma[0] =  y
       self.idx += 1
       
@factor_register(name='涨停后回踩均线', 
                   params=[{'name':'窗口长度','code':'N', 'default':6, 'desc':'存在涨停的时间窗口, 即几天内存在涨停'},
                           {'name':'均线','code':'MA', 'default': 10, 'desc':'均线类型'}],
                desc='强弱指标的值均在0与100之间。强弱指标保持高于50表示为强势市场，反之低于50表示为弱势市场。',
                factor_type='buy')
class ZtAndBackMA(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        datas = instance.datas #处理多只股票
        indicators = {}
        for data in datas[:-1]: #最后一个是benchmark
            zt_indicator  = ZtAndBackMAFactor(data, windows=int(self.N))
            sma = bt.indicators.SMA(data, period=int(self.MA))
            sma_indicator = data.close <= sma
            instance.sma = sma
            instance.zt = zt_indicator
            indicator = bt.And(zt_indicator, sma_indicator)
            indicators[data._name] = indicator
        return indicators
