from src.items.base_item import StockBaseItem
from dataclasses import dataclass


@dataclass
class TuShareStockItem(StockBaseItem):
    """股票列表基本信息"""
    ts_code	:str =  '-'	#TS代码

    symbol	:str =  '-'	#股票代码

    name	:str =  '-'	#股票名称

    area	:str =  '-'	#地域

    industry	:str =  '-'	#所属行业

    fullname	:str =  '-'	#股票全称F

    enname	:str =  '-'	#英文全称

    cnspell	:str =  '-'	#拼音缩写

    market	:str =  '-'	#市场类型

    exchange	:str =  '-'	#交易所代码

    curr_type	:str =  '-'	#交易货币

    list_status	:str =  '-'	#上市状态 L上市 D退市 P暂停上市

    list_date	:str =  '-'	#上市日期

    delist_date	:str =  '-'	#退市日期

    is_hs	:str =  '-'	#是否沪深港通标的，N否 H沪股通 S深股通

    act_name	:str =  '-'	#实控人名称

    act_ent_type	:str =  '-'	#实控人企业性质
    
@dataclass
class TuShareDailyDataItem(StockBaseItem):
    """日线行情"""
    ts_code	:str =  '-'	#股票代码
    trade_date	:str =  '-'	#交易日期
    open	:float=  0	#开盘价
    high	:float=  0	#最高价
    low	:float=  0	#最低价
    close	:float=  0	#收盘价
    pre_close	:float=  0	#昨收价(前复权)
    change	:float=  0	#涨跌额
    pct_chg	:float=  0	#涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
    vol	:float=  0	#成交量 （手）
    amount	:float=  0	#成交额 （千元）
    
@dataclass
class TuShareRealTimeQuoteItem(StockBaseItem):
    """实时盘口TICK快照(爬虫)"""
    name	:str =  '-'	#股票名称
    ts_code	:str =  '-'	#股票代码
    zsz: float = 0.0  # 总市值（元）
    ltsz: float = 0.0  # 流通市值（元）
    open	:float=  0	#开盘价
    pre_close	:float=  0	#昨收价
    price	:float=  0	#现价
    high	:float=  0	#今日最高价
    low	:float=  0	#今日最低价
    zhfu        :float = 0 #振幅
    zdfd       :float = 0 #涨跌幅度
    z53: str = '-'  # 归属概念板块名称
    z50: str = '-'  # 归属行业板块名称
    atr14:float = 0 # 14日加权平均振幅
    atr21:float = 0 #
    z52: str = '-'  # 归属地域板块名称
    hslv :float = 0 #换手率
    volume	:int =  0	#成交量（src=sina时是股，src=dc时是手）
    amount	:float=  0	#成交金额（元 CNY）
    bid	:float=  0	#竞买价，即“买一”报价（元）
    ask	:float=  0	#竞卖价，即“卖一”报价（元）
    b1_v	:float=  0	#委买一（量，单位：手，下同）
    b1_p	:float=  0	#委买一（价，单位：元，下同）
    b2_v	:float=  0	#委买二（量）
    b2_p	:float=  0	#委买二（价）
    b3_v	:float=  0	#委买三（量）
    b3_p	:float=  0	#委买三（价）
    b4_v	:float=  0	#委买四（量）
    b4_p	:float=  0	#委买四（价）
    b5_v	:float=  0	#委买五（量）
    b5_p	:float=  0	#委买五（价）
    a1_v	:float=  0	#委卖一（量，单位：手，下同）
    a1_p	:float=  0	#委卖一（价，单位：元，下同）
    a2_v	:float=  0	#委卖二（量）
    a2_p	:float=  0	#委卖二（价）
    a3_v	:float=  0	#委卖三（量）
    a3_p	:float=  0	#委卖三（价）
    a4_v	:float=  0	#委卖四（量）
    a4_p	:float=  0	#委卖四（价）
    a5_v	:float=  0	#委卖五（量）
    a5_p	:float=  0	#委卖五（价）
    zgb     :float=  0  #总股本
    ltgb    :float=  0  #流通股本
    time	:str =  '-'	#交易时间
    date	:str =  '-'	#交易日期
    code    :str = '-' #股票代码
    ssdate  :str = '-' #成立时间


    