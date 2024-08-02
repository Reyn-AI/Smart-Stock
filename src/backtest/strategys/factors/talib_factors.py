from src.utils.registy import factor_register, dynamic_factor_register
import backtrader as bt
from src.backtest.strategys.factors.base_factor import BaseFactor

@factor_register(name='资金流量指标(MFI)达到阈值', 
                   params=[{'name':'阈值','code':'threshold', 'default':50, 'desc':'大于阈值时买入或卖出'},
                           {'name':'MFI计算周期(天)','code':'timeperiod', 'default':14, 'desc':'MFI计算周期(天)'}],
                desc='资金流量指标(MFI)达到阈值执行买卖')
class TaLibMFI(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        datas = instance.datas #处理多只股票
        indicators = {}
        for data in datas[:-1]: #最后一个是benchmark
            mfi = bt.talib.MFI(data.high, data.low, data.close, data.volume, int(getattr(self,'timeperiod', 14)))
            if self.order_type==1:
                indicator = mfi >= float(getattr(self,'default', 50))
            else:
                indicator = mfi < float(getattr(self,'default', 50))
            indicators[data._name] = indicator
        return indicators

@dynamic_factor_register(name='n倍atr(止盈止损)因子', 
                   params=[{'name':'振幅1(日)','code':'atr1', 'default':14, 'desc':'N日振幅'},
                           {'name':'振幅2(日)','code':'atr2', 'default':21, 'desc':'N日振幅'},
                           {'name':'止损的atr倍数','code':'stop_loss_n', 'default':1, 'desc':'N日振幅'},
                           {'name':'止盈的atr倍数','code':'stop_win_n', 'default':0.5, 'desc':'N日振幅'}],
                desc='收益大于n倍平均atr止盈或小于-n倍atr止损',
                factor_type='sell')
class TaLibNAtr(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        instance.atr1 = bt.talib.ATR(data.high, data.low, data.close,getattr(self,'atr1', 14))
        instance.atr2 = bt.talib.ATR(data.high, data.low, data.close,getattr(self,'atr2', 21))
        return self.dynamic_judge
        
    def dynamic_judge(self, data, broker:bt.broker, *args, **kwargs):
        instance = kwargs.get('instance')
        mean_atr = (instance.atr1 + instance.atr2)/2
        profit = broker.getposition(data).price - data.close[0]
        if profit > (float(self.stop_win_n) * mean_atr) or profit < -(float(self.stop_loss_n) * mean_atr):
            return True
        
        return False


@factor_register(name='长期趋势中短期回调买入策略', 
                   params=[{'name':'长期窗口(日)','code':'win_long', 'default':60, 'desc':'长期趋势的时间窗口'},
                           {'name':'短期窗口(日)','code':'win_short', 'default':20, 'desc':'短期回调时间窗口'},
                           {'name':'角度阈值','code':'angle', 'default':5, 'desc':'窗口内k线角度大于多少认为是上升趋势'}],
                desc='对于长期趋势的股票短期回调时买入',
                factor_type='buy')
class TaLibAngle(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        datas = instance.datas #处理多只股票
        indicators = {}
        for data in datas[:-1]: #最后一个是benchmark
            angle = bt.talib.LINEARREG(data.close, timeperiod=int(getattr(self,'win_long', 60)))
            sma  = bt.indicators.SMA(data.close, period=int(getattr(self, 'win_short', 20)))
            indicator = bt.And(angle>float(self.angle), data.close<sma)
            indicators[data._name] = indicator
        return indicators



@factor_register(name='RSI超卖时买入策略', 
                   params=[{'name':'窗口长度','code':'timeperiod', 'default':6, 'desc':'RSI计算窗口长度'},
                           {'name':'阈值','code':'threshold', 'default': 15, 'desc':'RSI小于该阈值时买入'}],
                desc='强弱指标的值均在0与100之间。强弱指标保持高于50表示为强势市场，反之低于50表示为弱势市场。',
                factor_type='all')
class TaLibRSI(BaseFactor):
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        instance = kwargs.get('instance')
        datas = instance.datas #处理多只股票
        indicators = {}
        for data in datas[:-1]: #最后一个是benchmark
            RSI  = bt.talib.RSI(data.close, timeperiod=int(getattr(self, 'timeperiod', 6)))
            indicator = RSI <= float(self.threshold)
            indicators[data._name] = indicator
        return indicators


