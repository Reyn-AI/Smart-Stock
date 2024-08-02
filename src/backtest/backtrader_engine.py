from typing import List, Dict
from src.backtest.backtrade_params import BackTraderParams
import backtrader as bt
from src.utils.tushare_tool import backtrader_add_data_from_tushare, get_data_by_abu
import backtrader as bt
from src.backtest.custom_commission import MarketAStockCommission
from functools import partial

class BackTraderEngine:
    def __init__(self, 
                 params:BackTraderParams,
                 strategy:bt.Strategy=None,
                 analyzers:List[bt.Analyzer]=[bt.analyzers.TimeReturn, #收益率时序数据
                                             bt.analyzers.AnnualReturn, #年华收益率
                                             bt.analyzers.SharpeRatio, #夏普比率
                                             bt.analyzers.DrawDown, #回撤率
                                             bt.analyzers.Returns], 
                 singals:List[bt.Indicator]=[],
                 commission=None,
                 observers:List[bt.Observer]=[bt.observers.Broker,
                                              bt.observers.Benchmark]) -> None:
        
        self.params = params #基础参数
        self.strategy = strategy #交易策略
        self.singals = singals  #交易信号与stragegy二选一
        self.analyzers = analyzers #指标分析器
        self.commission = commission if commission is not None else MarketAStockCommission(stamp_duty=params.stamp_duty) #手续费
        self.observers = observers #观察器
        self.date_index = [] #时序列表
        if params.strategy_opt_param_dict is not None and len(params.strategy_opt_param_dict)>0:
            self.cerebro = bt.Cerebro(optdatas=True, optreturn=True)
            self.opt = True #优化参数
        else:
            self.cerebro = bt.Cerebro()
            self.opt = False
        #添加数据
        self._init_data()
        #添加策略
        self._init_strategy()
        #添加分析器
        self._init_analysis()
        #初始化交易参数
        self._init_commission()
        #初始化观察器
        self._init_observers()
    
    def _init_data(self):
        """初始化数据"""
        for code in self.params.stock_list:
            backtrader_add_data_from_tushare(cerebro=self.cerebro, code=code, start_date=self.params.start_date, end_date=self.params.end_date, api_type='qstock')
    
    def _init_observers(self):
        """初始化观察器"""
        for observer in self.observers:
            if observer.__name__ == 'Benchmark':
                # 添加业绩基准时，需要事先将业绩基准的数据添加给 cerebro
                data = backtrader_add_data_from_tushare(cerebro=self.cerebro, code=self.params.benchmark, start_date=self.params.start_date, end_date=self.params.end_date, api_type='qstock')
                self.date_index = data._dataname.index.strftime('%Y-%m-%d').to_list()
                # self.cerebro.addobserver(observer, data=data)
                self.cerebro.addanalyzer(bt.analyzers.TimeReturn,data=data, _name='benchmark')
                continue
            self.cerebro.addobserver(observer)
    
    def _init_analysis(self):
        """初始化分析器"""
        for analyzer in self.analyzers:
            self.cerebro.addanalyzer(analyzer, _name=str(analyzer.__name__))
    
    def _init_strategy(self):
        """添加策略"""
        if self.strategy is not None:
            self.strategy = partial(self.strategy, msg_queen=self.params.msg_queen)
            if self.opt:  #开启优化
                strategy_opt_param_dict = self.params.strategy_opt_param_dict
                strategy_name = self.params.strategy_opt_param_dict.get('name')
                assert strategy_name == f'{self.strategy}'
                params_str = []
                for name, value in strategy_opt_param_dict.get('params').items():
                    param_str = f"{name}={value}"
                    params_str.append(param_str)
                params_str = ','.join(params_str)
                expr = f"self.cerebro.optstrategy(self.strategy, {param_str})"
                eval(expr)
            else:
                self.cerebro.addstrategy(self.strategy)
        elif len(self.singals)>0:
            for singal in self.singals:
                self.cerebro.add_signal(singal)
    
    def _init_commission(self):
        """初始化交易参数"""
        self.cerebro.broker.setcash(self.params.cash) #初始化资金
        self.cerebro.broker.set_slippage_perc(perc=self.params.broker_params.slippage_perc) #初始化滑点
        self.commission.p.commission = self.params.broker_params.commission
        self.cerebro.broker.addcommissioninfo(self.commission) #初始化手续费
        if self.params.broker_params.size is not None and self.params.broker_params.size>100:
            self.cerebro.broker.set_filler(bt.broker.fillers.FixedSize(size=self.params.broker_params.size))
    
    def run(self):
        result = self.cerebro.run()
        self.results = result #存储返回结果
        return result