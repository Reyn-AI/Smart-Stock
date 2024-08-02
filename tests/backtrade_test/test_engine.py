from src.backtest.backtrader_engine import BackTraderEngine
from src.backtest.backtrade_params import BackTraderParams, BrokerParams, OrderParams
from src.backtest.strategys.ema_strategy import EMAStockStrategy
import backtrader as bt
import pandas as pd
from multiprocessing import Queue

def test_run():
    params = BackTraderParams(stock_list=['600640'], start_date='2023-01-01', end_date='2024-04-28', msg_queen=Queue())
    broker_params = BrokerParams()
    params.broker_params = broker_params
    engine = BackTraderEngine(params=params,
                              strategy=EMAStockStrategy)
    
    result = engine.run()
    strat = result[0]
    benchmark = []
    while(True):
        if engine.params.msg_queen.empty():
            break
        msg = engine.params.msg_queen.get()
        if msg['type']=='benchmark':
            benchmark.append((msg['value'], msg['date']))
    # 返回日度收益率序列
    breakpoint()
    daily_return = pd.Series(strat.analyzers.TimeReturn.get_analysis())
    print(daily_return)
    # 打印评价指标
    print("--------------- AnnualReturn -----------------")
    print(strat.analyzers.AnnualReturn.get_analysis())
    print("--------------- SharpeRatio -----------------")
    print(strat.analyzers.SharpeRatio.get_analysis())
    print("--------------- DrawDown -----------------")
    print(strat.analyzers.DrawDown.get_analysis())

test_run()