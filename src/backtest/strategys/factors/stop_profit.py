from src.utils.registy import dynamic_factor_register
import backtrader as bt
from src.backtest.strategys.factors.base_factor import BaseFactor

@dynamic_factor_register(name='静态止盈止损策略', 
                   params=[{'name':'止盈率','code':'stop_win', 'default':0.15, 'desc':'大于阈值时止盈卖出'},
                           {'name':'止损率','code':'stop_loss', 'default':0.05, 'desc':'小于阈值时止损卖出'}],
                   desc='收益率达到固定值卖出止盈',
                   factor_type='sell')
class StaticStopProfit(BaseFactor):
    
    def get_indicator(self, data, *args, **kwargs):
        super().get_indicator(data=data, *args, **kwargs)
        return self.dynamic_judge
    
    def dynamic_judge(self, data, broker:bt.broker, *args, **kwargs):
        """在next中执行"""
        instance = kwargs.get('instance')
        holding_cost = broker.getposition(data).price
        if holding_cost == 0:
            return False
        profit = (data.close[0]-holding_cost)/holding_cost
        if profit>float(getattr(self,'stop_win', 0.2)) or profit< -float(self.stop_loss):
            return True
        else:
            return False