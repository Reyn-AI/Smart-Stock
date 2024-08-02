"""数据加载器"""
import backtrader as bt
import pandas as pd
import datetime
from tqdm import tqdm
from src.backtest.tushare_feed import TuSharePandasFeed
from src.utils.common import format_ts_code

class TuShareDataLoaderJson:
    
    def __init__(self, 
                 json_path:str,
                 stock_code:list=[]
                 ):
        self.json_path = json_path
        self.stock_code = format_ts_code(stock_code)
        self.__pre_loader()
        
    def __pre_loader(self):
        """预先读取文件"""
        self.daily_price = pd.read_json(self.json_path)
        self.daily_price['trade_date'] = pd.to_datetime(self.daily_price['trade_date'], format='%Y%m%d')
        
    def load_json_tushare(self, cerebro:bt.Cerebro, from_date, end_date):
        """加载tushare格式json数据"""
        
        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        #%%

        # 按股票代码，依次循环传入数据
        for stock in tqdm(self.daily_price['ts_code'].unique()):
            # 日期对齐
            if self.stock_code is None or len(self.stock_code)==0 or (len(self.stock_code)>0 and stock in self.stock_code):            
                data = pd.DataFrame(self.daily_price['trade_date'].unique(), columns=['trade_date'])  # 获取回测区间内所有交易日
                df = self.daily_price.query(f"ts_code=='{stock}'")[
                    ['trade_date', 'open', 'high', 'low', 'close', 'vol', 'pre_close', 'change', 'pct_chg', 'amount']]
                df.columns = ['trade_date', 'open', 'high', 'low', 'close','vol', 'pre_close', 'change', 'pct_chg', 'amount']
                data_ = pd.merge(data, df, how='left', on='trade_date')
                data_.index = data_.trade_date
                data_.sort_index(inplace=True)
                # 缺失值处理：日期对齐时会使得有些交易日的数据为空，所以需要对缺失数据进行填充
                data_.loc[:, ['vol', 'amount']] = data_.loc[:, ['vol', 'amount']].fillna(0)
                data_.loc[:, ['open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg']] = data_.loc[:, ['open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg']].fillna(method='pad')
                data_.loc[:, ['open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg']] = data_.loc[:, ['open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg']].fillna(0)
                data_ = data_.rename(columns={'vol':'volume'})
                # 导入数据
                datafeed = TuSharePandasFeed(dataname=data_, fromdate=from_date,
                                            todate=end_date)
                cerebro.adddata(datafeed, name=stock)  # 通过 name 实现数据集与股票的一一对应
        return cerebro
    
    # print("All stock Done !")
