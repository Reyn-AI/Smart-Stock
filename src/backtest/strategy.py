"""回测策略"""
import backtrader as bt
import pandas as pd
from src.utils.tushare_tool import *
# 回测策略
class SingleStockStrategy(bt.Strategy):
    params = (('maperiod', 15),)
    
    def __init__(self, stock_code='600519.SH', msg_queen=None):
        self.stock_list = stock_code #需要回测的股票代码
        self.sma1 = bt.indicators.SimpleMovingAverage(self.data.close)
        self.ema1 = bt.indicators.ExponentialMovingAverage(self.data.close)
        self.close_over_sma = self.data.close > self.sma1
        self.close_over_ema = self.data.close > self.ema1
        self.sma_ema_diff = self.sma1 - self.ema1
        # 生成交易信号
        self.buy_sig = bt.And(self.close_over_sma, self.close_over_ema, self.close_over_ema>0)
        self.sell_sig = bt.And(self.sma_ema_diff<0)
        
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    
    def info(self):
        print('当前可用资金', self.broker.getcash())
        print('当前总资产', self.broker.getvalue())
        print('当前持仓量', self.broker.getposition(self.data).size)
        print('当前持仓成本', self.broker.getposition(self.data).price)
        # 也可以直接获取持仓
        print('当前持仓量', self.getposition(self.data).size)
        print('当前持仓成本', self.getposition(self.data).price)
       
    def next(self):
        close = self.data.close[0]
        unuse_money = self.broker.getcash()
        buy_size = (unuse_money*0.9//close)
        if self.buy_sig and buy_size>1:
            order = self.buy(self.data, size=buy_size)
        if self.sell_sig and self.broker.getposition(self.data).size:
            self.sell(self.data, size=self.broker.getposition(self.data).size)

    def notify_order(self, order):
        # 未被处理的订单
        # print('当前持仓量', self.broker.getposition(self.data).size)
        # print('当前持仓成本', self.broker.getposition(self.data).price)
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 已经处理的订单
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, ref:%.0f，Price: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f, Stock: %s' %
                    (order.ref,  # 订单编号
                     order.executed.price,  # 成交价
                     order.executed.value,  # 成交额
                     order.executed.comm,  # 佣金
                     order.executed.size,  # 成交量
                     order.data._name))  # 股票名称
                print('当前持仓量', self.broker.getposition(self.data).size)
            else:  # Sell
                self.log('SELL EXECUTED, ref:%.0f, Price: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f, Stock: %s' %
                         (order.ref,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          order.executed.size,
                          order.data._name))
                print('当前持仓量', self.broker.getposition(self.data).size)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    # cerebro = TuShareDataLoaderJson('/data/application/liqy/codes/gitee/smart-stock/data/test_data/day_k_line_000066_20230101-_20240401.json').load_json_tushare(cerebro, from_date='2023-04-01', end_date='2024-03-06')
    df = backtrader_add_data_from_tushare(cerebro=cerebro, code='000066', start_date='2022-01-01', end_date='2024-03-08')
    # 初始资金 100,000,000
    cerebro.broker.setcash(100000.0)
    # 佣金，双边各 0.0003
    cerebro.broker.setcommission(commission=0.0003)
    # 滑点：双边各 0.0001
    cerebro.broker.set_slippage_perc(perc=0.005)

    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl')  # 返回收益率时序数据
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')  # 年化收益率
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')  # 夏普比率
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')  # 回撤

    # 将编写的策略添加给大脑，别忘了 ！
    cerebro.addstrategy(SingleStockStrategy)

    # 启动回测
    result = cerebro.run()
    # 从返回的 result 中提取回测结果
    strat = result[0]
    # 返回日度收益率序列
    daily_return = pd.Series(strat.analyzers.pnl.get_analysis())
    # 打印评价指标
    print("--------------- AnnualReturn -----------------")
    print(strat.analyzers._AnnualReturn.get_analysis())
    print("--------------- SharpeRatio -----------------")
    print(strat.analyzers._SharpeRatio.get_analysis())
    print("--------------- DrawDown -----------------")
    print(strat.analyzers._DrawDown.get_analysis())
    print('当前可用资金', cerebro.broker.getcash())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
