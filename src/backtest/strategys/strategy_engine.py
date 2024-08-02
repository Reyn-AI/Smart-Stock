from typing import List, Dict
from src.backtest.strategys.base_strategys import BaseStockStrategy
import backtrader as bt
from src.backtest.strategys.size_strategy import AllInStrategy, BaseSizeStrategy
from src.utils.registy import CLS_REGISTRY_ADDRESS

class StrategyEngine(BaseStockStrategy):
    
    def __init__(self,
                 buy_singals: List,
                 sell_singals: List,
                 sell_size_strategy:BaseSizeStrategy=AllInStrategy(),
                 buy_size_strategy:BaseSizeStrategy=AllInStrategy(),
                 buy_combin_type:str='and',
                 sell_combin_type:str='and',
                 dynamic_buy_singals=[],
                 dynamic_sell_singals=[],
                 *args, **kwargs):
        """根据传参生成策略
            Args:
                buy_singals 买入信号组合 传入factor注册器中参数格式
                sell_singals 卖出信号组合 传入factor注册器中参数格式
                sell_size_strategy 买入仓位策略
                buy_size_strategy 卖出仓位策略
                buy_combin_type 买入条件组合方式 and/or
                sell_combin_type 卖出条件组合方式 and/or
                dynamic_buy_singals 动态买入策略
                dynamic_sell_singals 动态卖出策略
        """
        super().__init__(*args, **kwargs)
        buy_singals = self.gen_indicator(buy_singals, order_type=1)
        sell_singals = self.gen_indicator(sell_singals, order_type=-1)
        self.buy_combin_type = buy_combin_type
        self.sell_combin_type = sell_combin_type
        self.dynamic_buy_singals = self.gen_indicator(dynamic_buy_singals, order_type=1)
        self.dynamic_sell_singals = self.gen_indicator(dynamic_sell_singals, order_type=-1)
        self.buy_singal = {}
        self.sell_singal = {}
        if len(buy_singals)>0:
            self.buy_singal = self.deal_indicators(buy_singals, buy_combin_type)
        if len(sell_singals)>0:
            self.sell_singal = self.deal_indicators(sell_singals, sell_combin_type)
        self.buy_size_strategy = buy_size_strategy
        self.sell_size_strategy = sell_size_strategy
        
    def deal_indicators(self, singals: List[Dict], combine_type:str):
        """处理不同股票的交易信号"""
        stock_singals = {}
        if len(singals) == 0:
            return stock_singals
        if not isinstance(singals[0], dict):
            return singals
        for singal in singals:
            for name, indicator in singal.items():
                if name in stock_singals.keys():
                    stock_singals[name].append(indicator)
                else:
                    stock_singals[name] = [indicator]
        for k in stock_singals.keys():
            if combine_type.lower() == 'and':
                stock_singals[k] = bt.And(*stock_singals[k])
            else:
                stock_singals[k] = bt.Or(*stock_singals[k])
        return stock_singals
        
    def gen_indicator(self ,singals: List, order_type):
        """根据参数获取指示器"""
        singals_ = []
        for singal in singals:
            cls_name = singal.get('code')
            params = singal.get('params')
            cls_instance = CLS_REGISTRY_ADDRESS[cls_name](order_type=order_type)
            singals_.append(cls_instance.get_indicator(data=self.data, params=params, instance=self))
        return singals_
    
    def execute_dynamic_indicator(self, order_type, data):
        """执行动态策略组合或者结果"""
        if order_type == 1:
            if len(self.dynamic_buy_singals)==0:
                return True if self.buy_combin_type=='and' else False
            else:
                results = []
                for func in self.dynamic_buy_singals:
                    res = func(data=data, broker=self.broker, instance=self)
                    results.append(res)
                if self.buy_combin_type == 'and':
                    return all(results)
                else:
                    return any(results)
        else:
            if len(self.dynamic_sell_singals)==0:
                return True if self.sell_combin_type=='and' else False
            else:
                results = []
                for func in self.dynamic_sell_singals:
                    res = func(data=data, broker=self.broker, instance=self)
                    results.append(res)
                if self.sell_combin_type == 'and':
                    return all(results)
                else:
                    return any(results)
    
    
    def next(self):
        super().next()
        for data in self.datas[:-1]:
            if len(data._name.split('_'))>1: #跳过日频外数据
                continue
            self.data = data
            close = data.close[0]
            cash = self.broker.getcash()
            had_size = self.broker.getposition(data).size
            # self.info(f'angle:{self.angle.lines.real[0]}, sma:{self.sma.lines.sma[0]}')
            if had_size>0:
                if eval(f"self.sell_singal.get('{data._name}', True if len(self.dynamic_sell_singals)>0 and self.sell_combin_type=='and' else False) {self.sell_combin_type} self.execute_dynamic_indicator(order_type=-1, data=data)"):
                    sell_size = self.sell_size_strategy.compute(price=close, cash=cash, had_size=had_size, order_type=-1, data=data)
                    # order = self._sell(size=sell_size)
                    if sell_size>0:
                        order =self.sell(data, size=sell_size)
                        continue
            if eval(f"self.buy_singal.get('{data._name}', True if len(self.dynamic_buy_singals)>0 and self.buy_combin_type=='and' else False) {self.buy_combin_type} self.execute_dynamic_indicator(order_type=1, data=data)"):
                buy_size = self.buy_size_strategy.compute(price=close, cash=cash, had_size=had_size, order_type=1, data=data)
                # order = self._buy(size=buy_size)
                if buy_size>0:
                    order =self.buy(data, size=buy_size)

