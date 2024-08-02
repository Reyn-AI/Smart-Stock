"""回测策略"""
import backtrader as bt
import pandas as pd
from src.utils.tushare_tool import *
from multiprocessing import Queue
# 回测策略

class BaseStockStrategy(bt.Strategy):
    
    def __init__(self, msg_queen: Queue=None, *args, **kwargs):
        self.msg_queen = msg_queen
        self.logger = get_logger()
    
    def log(self, order, dt=None, order_type='sell'):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        txt = '【%s】成交价: %.2f, 成交额: %.2f, 手续费 %.2f, 成交量: %.2f, 股票名称: %s' % \
                (   order_type,
                    order.executed.price,  # 成交价
                    order.executed.value,  # 成交额
                    order.executed.comm,  # 佣金
                    order.executed.size,  # 成交量
                    order.data._name)
        msg = f"{dt.isoformat()}, {txt}"
        print(msg)
        if self.msg_queen is not None:
            self.msg_queen.put({"type":"msg", "data":f"{msg}"})
            self.msg_queen.put({'type':'order', 'data':{'date':dt.isoformat(),
                                                        'type':order_type,
                                                        'price':order.executed.price,
                                                        'name':order.data._name,
                                                        'volume':order.executed.size}})
            if order_type == 'sell':
                self.msg_queen.put({"type":"pnl", "data":{'code':order.data._name, 'pnl':order.executed.pnl}})
      
    def info(self, msg):
        # print('当前可用资金', self.broker.getcash())
        # print('当前总资产', self.broker.getvalue())
        # print('当前持仓量', self.broker.getposition(self.data).size)
        # print('当前持仓成本', self.broker.getposition(self.data).price)
        # # 也可以直接获取持仓
        # print('当前持仓量', self.getposition(self.data).size)
        # print('当前持仓成本', self.getposition(self.data).price)
        date = self.datas[0].datetime.date(0)
        print(f"{date}:{msg}")
        if self.msg_queen is not None:
            self.msg_queen.put({"type":"msg", "data":f"{date}:{msg}"})
        
    
    def notify_fund(self, cash, value, fundvalue, shares):
        # 当前现金、现有总价值、基金价值和股份份额
        pass

    def notify_order(self, order):
        # 未被处理的订单
        # print('当前持仓量', self.broker.getposition(self.data).size)
        # print('当前持仓成本', self.broker.getposition(self.data).price)
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 已经处理的订单
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(order=order, order_type='buy')  # 股票名称
                self.info(f'当前持仓量[{order.data._name}]:{self.broker.getposition(self.data).size} 持仓成本: {self.broker.getposition(order.data).price}')
            else:  # Sell
                self.log(order=order, order_type='sell')
                self.info(f"交易盈亏[{order.data._name}]: {order.executed.pnl}")
                self.info(f'当前持仓量[{order.data._name}]:{self.broker.getposition(self.data).size}')
    
    def _buy(self, size, buy_type=None):
        """下买单"""
        order =self.buy(self.data, size=size)
        return order
    def _sell(self, size, buy_type=None):
        """下买单"""
        order =self.sell(self.data, size=size)
        return order
       
    def next(self):
        self.record_metric()
        
    def record_metric(self):
        """记录相关指标"""
        date = self.datas[0].datetime.date(0)
        if self.msg_queen is not None:
            # if hasattr(self.stats, 'benchmark'):
            #     self.msg_queen.put({'type':'benchmark', 'value':self.stats.benchmark[0],'date':date})
            if hasattr(self.stats, 'broker'):
                self.msg_queen.put({'type':'broker_cash', 'value':self.stats.broker.cash[0]}) #可用现金 self.statas获取观察器
                self.msg_queen.put({'type':'broker_sum', 'value':self.stats.broker.value[0]}) #总资产
    
