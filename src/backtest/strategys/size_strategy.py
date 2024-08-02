"""仓位策略"""
from typing import List, Dict
import abc
from src.utils.registy import size_strategy_register
from scipy import stats

class BaseSizeStrategy(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        params = kwargs.get('params', [])
        self.set_params(params)
        
    def set_params(self, params:List[Dict]):
        """设置属性"""
        for param in params:
            code = param.get('code')
            default = param.get('default')
            setattr(self, code, default)
    
    def compute(self, cash: float, price: float, had_size:int, order_type:int, **kwargs):
        pass

@size_strategy_register(name='全仓买卖策略', params=[], desc='全仓买入/卖出')
class AllInStrategy(BaseSizeStrategy):
    
    def compute(self, cash: float, price: float, had_size:int, order_type:int, **kwargs):
        """
            Args:
                cash 现金
                price 当前价格
                had_size 当前持仓数量
                order_type 买(1)or卖(-1)
        """
        if order_type==1:
            buy_size = (cash*0.9//price)
            buy_size = buy_size - buy_size%100
            return buy_size
        else:
            return had_size


@size_strategy_register(name='自定义仓位', params=[{'name':'仓位比例(%)', 'code':'ratio', 'default':100}], desc='按自定义的仓位比例进行买卖')
class CustomSizeStrategy(BaseSizeStrategy):
    
    def compute(self, cash: float, price: float, had_size:int, order_type:int, **kwargs):
        """
            Args:
                cash 现金
                price 当前价格
                had_size 当前持仓数量
                order_type 买(1)or卖(-1)
        """
        if order_type==1:
            buy_size = (cash*0.9//price)*(getattr(self,'ratio',100)/100)
            buy_size = buy_size - buy_size%100
            return buy_size
        else:
            sell_size = had_size*(getattr(self,'ratio',100)/100) - - buy_size%100
            return sell_size


@size_strategy_register(name='kelly仓位策略', params=[{'name':'仓位胜率', 'code':'win_rate', 'default':0.5},
                                                    {'name':'平均获利期望', 'code':'gains_mean', 'default':0.2},
                                                    {'name':'平均亏损期望', 'code':'losses_mean', 'default':0.1},
                                                    {'name':'最大仓位限制', 'code':'max_pos', 'default':0.98}],
                                                    desc='在一个期望收益为正的重复性赌局或者重复性投资中，每一期应该下注的最优比例',
                                                    factor_type='buy'
                                            )
class KellySizeStrategy(BaseSizeStrategy):
    
    def compute(self, cash: float, price: float, had_size:int, order_type:int, **kwargs):
        """
            Args:
                cash 现金
                price 当前价格
                had_size 当前持仓数量
                order_type 买(1)or卖(-1)
        """
        max_pos = self.max_pos #最大仓位比例
         # 败率
        loss_rate = 1 - self.win_rate
        # kelly计算出仓位比例
        kelly_pos = self.win_rate - loss_rate / (self.gains_mean / self.losses_mean)
        # 最大仓位限制，依然受上层最大仓位控制限制，eg：如果kelly计算出全仓，依然会减少到75%，如修改需要修改最大仓位值
        kelly_pos = max_pos if kelly_pos > max_pos else kelly_pos
        # 结果是买入多少个单位
        buy_size = cash * kelly_pos / price
        buy_size = buy_size - buy_size%100
        return buy_size

@size_strategy_register(name='价格位置仓位策略', params=[{'name':'默认平均仓位比例', 'code':'pos_base', 'default':0.9, 'desc':'范围0-1'},
                                                    {'name':'时间窗口长度(天)', 'code':'past_day_cnt', 'default':15, 'desc':'利用过去多少天的价格计算'},
                                                    {'name':'最大仓位限制', 'code':'max_pos', 'default':0.98, 'desc':'最大的仓位限制'}],
                                                    desc='根据买入价格在之前一段时间的价格位置来决策仓位大小',
                                                    factor_type='buy'
                                            )
class PtSizeStrategy(BaseSizeStrategy):
    """
        示例价格位置仓位管理类：

        根据买入价格在之前一段时间的价格位置来决策仓位大小

        假设过去一段时间的价格为[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        如果当前买入价格为2元：则买入仓位配比很高(认为均值回复有很大向上空间)
        如果当前买入价格为9元：则买入仓位配比很低(认为均值回复向上空间比较小)
    """
    
    def compute(self, cash: float, price: float, had_size:int, order_type:int, **kwargs):
        """
            Args:
                cash 现金
                price 当前价格
                had_size 当前持仓数量
                order_type 买(1)or卖(-1)
        """
        data = kwargs.get('data')
        last_list = []
        # self.kl_pd_buy为买入当天的数据，获取之前的past_day_cnt天数据
        for i in range(0, self.past_day_cnt,):
            last_list.append(data[-i])
        if last_list is None or len(last_list):
            precent_pos = self.pos_base
        else:
            # 使用percentileofscore计算买入价格在过去的past_day_cnt天的价格位置
            precent_pos = stats.percentileofscore(last_list, price)
            precent_pos = (1 + (50.0 - precent_pos) / 100) * self.pos_base
        # 最大仓位限制，依然受上层最大仓位控制限制，eg：如果算出全仓，依然会减少到75%，如修改需要修改最大仓位值
        precent_pos = self.max_pos if precent_pos > self.max_pos else precent_pos
        # 结果是买入多少个单位（股，手，顿，合约）
        buy_size = cash * precent_pos / price
        buy_size = buy_size - buy_size%100
        return buy_size
        