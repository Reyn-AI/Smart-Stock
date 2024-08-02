from typing import List, Dict, Union
from dataclasses import dataclass
from multiprocessing import Queue

@dataclass
class BaseTraderParams:
    """基础参数类"""
    start_date:str #回测开始日期
    end_date:str #回测结束日期
    stock_list: Union[List, str] = None
    cash:float = 100000
    stamp_duty:float = 2.5/10000 #印花税


@dataclass
class BrokerParams:
    commission:float = 3/10000 #手续费
    slippage_perc:float = 0.001 #滑点百分比 0.1% 买入卖出都要加上滑点
    size:float = None #最大固定成交量限制, 超出当日最大成交量部分不会被成交
    trading_opportunity:str = None #交易时机默认当日下单次日开盘价成交，’cheat_on_close(当日下单当日收盘成交)‘|'cheat_on_open(当日下单当日开盘成交)'

@dataclass
class OrderParams:
    '''
    Order.Market
        市价单，以当时市场价格成交的订单，不需要自己设定价格。市价单能被快速达成交易，防止踏空，尽快止损/止盈；
        按下一个 Bar （即生成订单的那个交易日的下一个交易日）的开盘价来执行成交；
        例：self.buy(exectype=bt.Order.Market)

    Order.Close
        和 Order.Market 类似，也是市价单，只是成交价格不一样；
        按下一个 Bar 的收盘价来执行成交；
        例：self.buy(exectype=bt.Order.Close) 

    Order.Limit
        限价单，需要指定成交价格，只有达到指定价格（limit Price）或有更好价格时才会执行，即以指定价或低于指点价买入，以指点价或更高指定价卖出；
        在订单生成后，会通过比较 limit Price 与之后 Bar 的 open\high\low\close 行情数据来判断订单是否成交。
        如果下一个 Bar 的 open 触及到指定价格 limit Price，就以 open 价成交，订单在这个 Bar 的开始阶段就被执行完成；
        如果下一个 Bar 的 open 未触及到指定价格 limit Price，但是 limit Price 位于这个 bar 的价格区间内 （即 low ~  high），就以 limit Price 成交；
        例：self.buy(exectype=bt.Order.Limit, price=price, valid=valid) 

    Order.Stop
        止损单，需要指定止损价格（Stop Price），一旦股价突破止损价格，将会以市价单的方式成交；
        在订单生成后，也是通过比较 Stop Price 与之后 Bar 的 open\high\low\close 行情数据来判断订单是否成交。
        如果下一个 Bar 的 open 触及到指定价格 limit Price，就以 open 价成交；
        如果下一个 Bar 的 open 未触及到指定价格 Stop Price，但是 Stop Price 位于这个 bar 的价格区间内 （即 low ~ high），就以 Stop Price 成交；
        例：self.buy(exectype=bt.Order.Stop, price=price, valid=valid) 

    Order.StopLimit
        止损限价单，需要指定止损价格（Stop price）和限价（Limit Price），一旦股价达到设置的止损价格，将以限价单的方式下单；
        在下一个 Bar，按 Order.Stop 的逻辑触发订单，然后以 Order.Limit 的逻辑执行订单；
        例：self.buy(exectype=bt.Order.StopLimit, price=price, valid=valid, plimit=plimit)

    Order.StopTrail
        跟踪止损订单，是一种止损价格会自动调整的止损单，调整范围通过设置止损价格和市场价格之间的差价来确定。
        差价即可以用金额 trailamount 表示，也可以用市价的百分比 trailpercent  表示；
        如果是通过 buy 下达了买入指令，就会“卖出”一个跟踪止损单，在市场价格上升时，止损价格会随之上升；
        若股价触及止损价格时，会以市价单的形式执行订单；若市场价格下降或保持不变，止损价格会保持不变；
        如果是通过 sell 下达卖出指令，就会“买入”一个跟踪止损单，在市场价格下降时，止损价格会随之下降；
        若股价触及止损价格时，会以市价单的形式执行订单；但是当市场价格上升时，止损价格会保持不变；
        例：self.buy(exectype=bt.Order.StopTrail, price=xxx, trailamount=xxx)

    Order.StopTrailLimit
        跟踪止损限价单，是一种止损价格会自动调整的止损限价单，订单中的限价 Limit Price 不会发生变动，
        止损价会发生变动，变动逻辑与上面介绍的跟踪止损订单一致；
        例：self.buy(exectype=bt.Order.StopTrailLimit, plimit=xxx, trailamount=xxx) 
    '''
    exectype:str='bt.Order.Market' #市价单，以当时市场价格成交的订单，不需要自己设定价格。Order.Close Order.Limit Order.Stop
    price:float = None #限单价、止损价 价格
    plimit:float = None
    valid:str = None #订单失效时间
    

@dataclass
class BackTraderParams(BaseTraderParams):
    """基础配置"""
    broker_params:BrokerParams = None
    order_params:OrderParams = None
    strategy_opt_param_dict:Dict = None #策略优化参数字典，针对指定策略做优化格式: {"name":策略名, 'params':{'p_name':'参数名', 'value':'range(5,25,5)'}} 参数值通常是个range范围
    benchmark:str = '上证指数'
    msg_queen:Queue = None #消息传递队列

