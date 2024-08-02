from src.backtest.strategys.strategy_engine import StrategyEngine
from src.backtest.strategys.factors.talib_factors import TaLibMFI
from src.backtest.backtrader_engine import BackTraderEngine

from src.utils.tushare_tool import *
import backtrader as bt
from src.utils.registy import *
from functools import partial
from src.backtest.backtrade_params import BackTraderParams, BrokerParams, OrderParams
from multiprocessing import Queue
from src.backtest.strategys.factors import *

def test_strategy_engine():
    buys = {x['code']:x for x in BUY_FACTOR_REGISTRY}
    sells = {x['code']:x for x in SELL_FACTOR_REGISTRY}
    dyn_sells = {x['code']:x for x in DYNAMIC_SELL_FACTOR_REGISTRY}
    buy = [buys.get('ZtAndBackMA')]
    sell = [sells.get('RSRSIndicator')]
    # sell = []
    # dynamic_sell = [dyn_sells.get('StaticStopProfit')]
    strategy = partial(StrategyEngine,buy_singals=buy, sell_singals=sell, dynamic_sell_singals=[])
    
    params = BackTraderParams(stock_list=['001696'], start_date='2024-03-27', end_date='2024-08-01', msg_queen=Queue())
    broker_params = BrokerParams()
    params.broker_params = broker_params
    engine = BackTraderEngine(params=params,
                              strategy=strategy)
    
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
    print('当前可用资金', engine.cerebro.broker.getcash())
    print('当前总资产', engine.cerebro.broker.getvalue())
test_strategy_engine()