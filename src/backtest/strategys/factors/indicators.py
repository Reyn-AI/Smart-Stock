from src.utils.registy import factor_register, dynamic_factor_register
import backtrader as bt
from src.backtest.strategys.factors.base_factor import BaseFactor
from .custom_factors import *
import numpy as np
from sklearn.metrics import r2_score
from array import array
np.random.seed(0) #保证随机数生成的一致性


@factor_register(name='均线突破策略', 
                   params=[{'name':'N日均线','code':'threshold', 'default':10, 'desc':'突破n日均线买入/卖出'}],
                desc='突破均线后买入或卖出')
class EMA(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        datas = instance.datas #处理多只股票
        indicators = {}
        for data in datas[:-1]: #最后一个是benchmark
            sma = bt.indicators.SMA(data.close, period=getattr(self,'threshold', 10))
            if self.order_type==1:
                indicator = data.close > sma
            else:
                indicator = data.close < sma
            indicators[data._name] = indicator
        return indicators

@factor_register(name='均线金叉', 
                   params=[{'name':'均线1(日)','code':'line1', 'default':5, 'desc':'突破均线'},
                           {'name':'均线2(日)','code':'line2', 'default':10, 'desc':'被突破均线'}],
                desc='均线1突破均线2后买入/卖出')
class EMALine2(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        datas = instance.datas #处理多只股票
        indicators = {}
        for data in datas[:-1]: #最后一个是benchmark
            line1 = bt.indicators.SMA(data.close, period=int(getattr(self, 'line1', 5)))
            line2 = bt.indicators.SMA(data.close, period=int(getattr(self, 'line2', 10)))
            if self.order_type==1:
                indicator = line1>line2
            else:
                indicator = line1<line2
            indicators[data._name] = indicator
        return indicators

@dynamic_factor_register(name='连续N天放量上涨', 
                   params=[{'name':'时间窗口N','code':'n', 'default':3, 'desc':'连续N天放量上涨'}],
                desc='连续N天放量上涨且无长上影线买入', factor_type='buy')
class VolumeAndPrice(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        return self.dynamic_judge
    
    def dynamic_judge(self, data, broker:bt.broker, *args, **kwargs):
        """在next中执行"""
        volumes = []
        prices = []
        self.n = int(self.n)
        for i in range(0, self.n):
            volumes.append(data.volume[-i])
            prices.append(data.close[-i])
        flag_vol = all(y > x for y, x in zip(volumes, volumes[1:]))
        flag_price = all(y > x for y, x in zip(prices, prices[1:]))
        high = data.high[0]
        close = data.close[0]
        flag =  flag_vol and flag_price and (high - close)/close <1/100
        return flag


@factor_register(name='PSY交易策略', 
                   params=[{'name':'时间窗口N','code':'n', 'default':14, 'desc':'N 天内上涨天数'},
                           {'name':'阈值','code':'threshold', 'default':25, 'desc':'买入时低于阈值买入, 卖出时低于阈值卖出'}],
                desc='PSY 指标的取值范围在 0 到 100 之间。当 PSY 值超过 85 时，表明市场处于超买状态，可能会出现回调；当 PSY 值低于 15 时，表明市场处于超卖状态，可能会出现反弹。')
class PSYIndicator(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        datas = instance.datas #处理多只股票
        indicators = {}
        for data in datas[:-1]: #最后一个是benchmark
            instance.psy = PSY(data.change, period = int(self.n))
            if self.order_type == 1:
                indicator = instance.psy<= float(self.threshold)
            else:
                indicator = instance.psy > float(self.threshold)
            indicators[data._name] = indicator
        return indicators
    

class PSY(bt.Indicator):
    lines = ('psy',)
    params = (('period', 14),)

    def next(self):
        period_data = self.data.get(size=self.p.period)
        psy = 0
        for d in period_data:
            if d>0:
                psy += 1
        if len(period_data)==self.p.period:
            self.lines.psy[0] = 100*psy / self.p.period
        else:
            self.lines.psy[0] = np.nan

@factor_register(name='WR超买/超卖策略', 
                   params=[{'name':'窗口长度','code':'timeperiod', 'default':14, 'desc':'WR计算窗口长度'},
                           {'name':'阈值','code':'threshold', 'default': -70, 'desc':'买入策略时高于阈值买入/卖出策略时低于阈值卖出'}],
                desc='WMS表示的是市场处于超买还是超卖状态。范围[-100, 0], 越接近0表示越超卖',
                factor_type='all')
class TaLibWR(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        datas = instance.datas #处理多只股票
        indicators = {}
        for data in datas[:-1]: #最后一个是benchmark
            name = data._name
            WR  = bt.indicators.WilliamsR(data, period=int(getattr(self, 'timeperiod', 14)))
            setattr(instance, f"WR_{name}", WR)
            if self.order_type==1:
                indicator = WR<=float(self.threshold) #
            else:
                indicator = WR>float(self.threshold)
            indicators[name] = indicator
        return indicators


@factor_register(name='RSRS相对撑压线', 
                params=[{'name':'时间窗口N','code':'n', 'default':16, 'desc':'时间窗口长度'},
                        {'name':'观察期时间窗口M','code':'m', 'default':300, 'desc':'RSRS观察期时间窗口长度'},
                           {'name':'阈值','code':'threshold', 'default':0.7, 'desc':'当RSRS右偏标准分大于0.7时，买入并持有，当RSRS右偏标准分小于-0.7时，则卖出平仓'}
                        ],
                
                desc='RSRS')
class RSRSIndicator(BaseFactor):
    
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        datas = instance.datas #处理多只股票
        indicators = {}
        for data in datas[:-1]: #最后一个是benchmark
            instance.rsrs = RSRSFactor(data, N = int(self.n), M=int(self.m))
            if self.order_type == 1:
                indicator = instance.rsrs >= float(self.threshold)
            else:
                indicator = instance.rsrs < float(self.threshold)
            indicators[data._name] = indicator
        return indicators
    
class RSRSFactor(bt.Indicator):
    lines = ('rsrs',)
    params = (('N', 16), ('M', 300), ('min_M', 20)) #N:窗口长度， M 标准分长度

    def __init__(self):
        self.rsk_std_score = RSRS()(self.data.high.array, self.data.low.array)
        # self.l.rsrs.array = array('d',self.rsk_std_score.tolist())
        # self.l.rsrs.idx = 0
        self.idx = 0
        
    def next(self):
       y = self.rsk_std_score[self.idx]
       self.l.rsrs[0] =  y
       self.idx += 1
