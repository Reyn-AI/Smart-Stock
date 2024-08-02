import backtrader as bt

class TuSharePandasFeed(bt.feeds.PandasData):
    lines = ('pre_close', 'change') # 要添加的线
    # 设置 line 在数据源上的列位置
    params=(
             ('pre_close', -1),
             ('change', -1)
            )
    # -1表示自动按列明匹配数据，也可以设置为线在数据源中列的位置索引