import backtrader as bt

class MarketAStockCommission(bt.CommInfoBase):
    """A股手续费"""
    params = (
                ('stocklike', True), # 指定为股票模式
                ('commtype', bt.CommInfoBase.COMM_PERC), # 使用百分比费用模式
                ('percabs', True), # commission 不以 % 为单位
                ('stamp_duty', 0.00025), # 印花税默认为 0.025%
             ) 
    
    # 自定义费用计算公式
    def _getcommission(self, size, price, pseudoexec):
            if size > 0: # 买入时，只考虑佣金
                if self.p.percabs:
                    return max(abs(size) * price * self.p.commission, 5) #最少5元
                else:
                    return max(abs(size) * price * self.p.commission*0.01, 5) #最少5元
            elif size < 0: # 卖出时，同时考虑佣金和印花税
                if self.p.percabs:
                    return max(abs(size) * price * self.p.commission, 5) + abs(size) * price *self.p.stamp_duty
                else:
                    return max(abs(size) * price * self.p.commission*0.01, 5) + abs(size) * price *self.p.stamp_duty
            else:
                return 0


if __name__ == '__main__':
    com = MarketAStockCommission()
