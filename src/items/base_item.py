"""数据实体类"""

from dataclasses import dataclass


@dataclass
class StockBaseItem:
    """item基类"""


@dataclass
class WZWStockItem(StockBaseItem):
    """歪枣网股票基本信息"""

    code: str = '-'  # 股票代码
    name: str = '-'  # 股票名称
    stype: int = 0  # 股票类型，1：深证股票，2：上证股票，3：北证股票，4：港股
    hsgt: int = 0  # 沪深港通，1：沪股通（港>沪）、2：深股通（港>深）、3：港股通（沪>港）、4：港股通（深>港）、5：港股通（深>港或沪>港）
    bk: str = '-'  # 所属板块，个股包括主板、创业板、科创板
    roe: float = 0.0  # ROE
    zgb: float = 0.0  # 总股本（股）
    ltgb: float = 0.0  # 流通股本（股）
    ltsz: float = 0.0  # 流通市值（元）
    zsz: float = 0.0  # 总市值（元）
    ssdate: str = '-'  # 上市日期
    z50: str = '-'  # 归属行业板块名称
    z52: str = '-'  # 归属地域板块名称
    z53: str = '-'  # 归属概念板块名称


@dataclass
class WZWStockCategoryItem(StockBaseItem):
    """股票分类数据"""

    code: str = '-'  # 股票代码
    name: str = '-'  # 股票名称
    stype: int = 0  # 股票类型，1：深证股票，2：上证股票，3：北证股票，4：港股
    hsgt: int = 0  # 沪深港通，1：沪股通（港>沪）、2：深股通（港>深）、3：港股通（沪>港）、4：港股通（深>港）、5：港股通（深>港或沪>港）
    bk: str = '-'  # 所属板块，个股包括主板、创业板、科创板
    roe: float = 0.0  # ROE
    zgb: float = 0.0  # 总股本（股）
    ltgb: float = 0.0  # 流通股本（股）
    ltsz: float = 0.0  # 流通市值（元）
    zsz: float = 0.0  # 总市值（元）
    ssdate: str = '-'  # 上市日期
    z50: str = '-'  # 归属行业板块名称
    z52: str = '-'  # 归属地域板块名称
    z53: str = '-'  # 归属概念板块名称


@dataclass
class WZWCalendarItem(StockBaseItem):
    """歪枣网股市日历信息"""

    mtype: int = 0  # 市场类型
    tdate: str = '-'  # 交易时间
    isopen: int = 0  # 是否休市，1：半天休市，2：全体休市，3：交易
    mkt: str = '-'  # 市场名称
    holiday: str = '-'  # 休市原因
    lastdate: str = '-'  # 前一个交易日
    nextdate: str = '-'  # 后一个交易日


@dataclass
class WZWFoudFlowItem(StockBaseItem):
    """资金流信息"""

    code: str = '-'  # 股票代码
    tdate: str = '-'  # 交易时间
    price: float = 0.0  # 最新价（元）
    zdfd: float = 0.0  # 涨跌幅度（%）
    zded: float = 0.0  # 涨跌额度（元）
    jys: int = 0  # 证券交易所
    name: str = '-'  # 股票名称
    z118: float = 0.0  # 今日主力净流入-净占比（%）
    zljlr: float = 0.0  # 今日主力净流入-净额（元）
    cddlr: float = 0.0  # 今日超大单流入（元）
    cddlc: float = 0.0  # 今日超大单流出（元）
    cddjlr: float = 0.0  # 今日超大单净流入-净额（元）
    z30: float = 0.0  # 今日超大单净流入-净占比（%）
    ddlr: float = 0.0  # 今日大单流入（元）
    ddlc: float = 0.0  # 今日大单流出（元）
    ddjlr: float = 0.0  # 今日大单净流入-净额（元）
    z33: float = 0.0  # 今日大单净流入-净占比（%）
    zdlr: float = 0.0  # 今日中单流入（元）
    zdlc: float = 0.0  # 今日中单流出（元）
    zdjlr: float = 0.0  # 今日中单净流入-净额（元）
    z36: float = 0.0  # 今日中单净流入-净占比（%）
    xdlr: float = 0.0  # 今日小单流入（元）
    xdlc: float = 0.0  # 今日小单流出（元）
    xdjlr: float = 0.0  # 今日小单净流入-净额（元）
    z39: float = 0.0  # 今日小单净流入-净占比（%）
    z71: float = 0.0  # 3日涨跌幅（%）
    z199: float = 0.0  # 3日主力净流入-净额（元）
    z200: float = 0.0  # 3日主力净流入-净占比（%）
    z201: float = 0.0  # 3日超大单净流入-净额（元）
    z202: float = 0.0  # 3日超大单净流入-净占比（%）
    z203: float = 0.0  # 3日大单净流入-净额（元）
    z204: float = 0.0  # 3日大单净流入-净占比（%）
    z205: float = 0.0  # 3日中单净流入-净额（元）
    z206: float = 0.0  # 3日中单净流入-净占比（%）
    z207: float = 0.0  # 3日小单净流入-净额（元）
    z208: float = 0.0  # 3日小单净流入-净占比（%）
    zf05: float = 0.0  # 5日涨跌幅（%）
    z98: float = 0.0  # 5日主力净流入-净额（元）
    z99: float = 0.0  # 5日主力净流入-净占比（%）
    z100: float = 0.0  # 5日超大单净流入-净额（元）
    z101: float = 0.0  # 5日超大单净流入-净占比（%）
    z102: float = 0.0  # 5日大单净流入-净额（元）
    z103: float = 0.0  # 5日大单净流入-净占比（%）
    z104: float = 0.0  # 5日中单净流入-净额（元）
    z105: float = 0.0  # 5日中单净流入-净占比（%）
    z106: float = 0.0  # 5日小单净流入-净额（元）
    z107: float = 0.0  # 5日小单净流入-净占比（%）
    zf10: float = 0.0  # 10日涨幅（%）
    z108: float = 0.0  # 10日主力净流入-净额（元）
    z109: float = 0.0  # 10日主力净流入-净占比（%）
    z110: float = 0.0  # 10日超大单净流入-净额（元）
    z111: float = 0.0  # 10日超大单净流入-净占比（%）
    z112: float = 0.0  # 10日大单净流入-净额（元）
    z113: float = 0.0  # 10日大单净流入-净占比（%）
    z114: float = 0.0  # 10日中单净流入-净额（元）
    z115: float = 0.0  # 10日中单净流入-净占比（%）
    z116: float = 0.0  # 10日小单净流入-净额（元）
    z117: float = 0.0  # 10日小单净流入-净占比（%）


@dataclass
class WZWBaseMetricItem(StockBaseItem):
    """基础指标信息"""

    code: str = '-'  # 股票代码
    tdate: str = '-'  # 交易时间
    price: float = 0.0  # 最新价（元）
    zdfd: float = 0.0  # 涨跌幅度（%）
    zded: float = 0.0  # 涨跌额度（元）
    cjl: float = 0.0  # 成交量（手）
    cje: float = 0.0  # 成交额（元）
    zhfu: float = 0.0  # 振幅（%）
    hslv: float = 0.0  # 换手率（%）
    dsyl: float = 0.0  # 市盈率TTM
    lbi: float = 0.0  # 量比
    name: str = '-'  # 股票名称
    zgj: float = 0.0  # 最高价（元）
    zdj: float = 0.0  # 最低价（元）
    jrkpj: float = 0.0  # 今日开盘价（元）
    zrspj: float = 0.0  # 昨日收盘价（元）
    zsz: float = 0.0  # 总市值（元）
    ltsz: float = 0.0  # 流通市值（元）
    z4: float = 0.0  # 涨速
    sjlv: float = 0.0  # 市净率（%）
    zf60: float = 0.0  # 60日涨幅（%）
    zfy: float = 0.0  # 今年以来涨幅（%）
    ssdate: str = '-'  # 上市日期
    weibi: float = 0.0  # 委比（%）
    wpan: float = 0.0  # 外盘（手）
    npan: float = 0.0  # 内盘（手）
    roe: float = 0.0  # ROE
    zgb: float = 0.0  # 总股本（股）
    ltgb: float = 0.0  # 流通股本（股）
    zys: float = 0.0  # 总营收（元）
    zystb: float = 0.0  # 总营收同比（%）
    jlr: float = 0.0  # 净利润
    mgwfplr: float = 0.0  # 每股未分配利润
    mlil: float = 0.0  # 毛利率
    fzl: float = 0.0  # 负债率
    z24: float = 0.0  # 股东权益
    mggjj: float = 0.0  # 每股公积金（元）
    zf05: float = 0.0  # 5日涨跌幅（%）
    zf20: float = 0.0  # 20日涨幅（%）
    mgsy: float = 0.0  # 每股收益（元）
    mgjzc: float = 0.0  # 每股净资产
    jsyl: float = 0.0  # 市盈率（静）
    ttmsyl: float = 0.0  # 市盈率（TTM）
    z71: float = 0.0  # 3日涨跌幅（%）
    jlil: float = 0.0  # 净利率
    z73: float = 0.0  # 市销率TTM
    z74: float = 0.0  # 市现率TTM
    z75: float = 0.0  # 总营业收入TTM
    z76: str = '-'  # 股息率
    jzc: float = 0.0  # 净资产
    z79: float = 0.0  # 净资产收益率TTM
    z80: float = 0.0  # 净利润TTM
    zf10: float = 0.0  # 10日涨幅（%）
    ztj: float = 0.0  # 涨停价（元）
    dtj: float = 0.0  # 跌停价（元）
    jjia: float = 0.0  # 均价（元）


@dataclass
class WZWStockDailyQuotationItem(StockBaseItem):
    """每日行情信息"""

    ode: str = '-'  # 股票代码
    tdate: str = '-'  # 交易时间
    price: float = 0.0  # 最新价（元）
    zdfd: float = 0.0  # 涨跌幅度（%）
    zded: float = 0.0  # 涨跌额度（元）
    cjl: float = 0.0  # 成交量（手）
    cje: float = 0.0  # 成交额（元）
    zhfu: float = 0.0  # 振幅（%）
    hslv: float = 0.0  # 换手率（%）
    dsyl: float = 0.0  # 市盈率（动态）
    lbi: float = 0.0  # 量比
    name: str = '-'  # 股票名称
    zgj: float = 0.0  # 最高价（元）
    zdj: float = 0.0  # 最低价（元）
    jrkpj: float = 0.0  # 今日开盘价（元）
    zrspj: float = 0.0  # 昨日收盘价（元）
    zsz: float = 0.0  # 总市值（元）
    ltsz: float = 0.0  # 流通市值（元）
    sjlv: float = 0.0  # 市净率（%）
    zf60: float = 0.0  # 60日涨幅（%）
    zfy: float = 0.0  # 今年以来涨幅（%）
    ssdate: str = '-'  # 上市日期
    weibi: float = 0.0  # 委比（%）
    wpan: float = 0.0  # 外盘（手）
    npan: float = 0.0  # 内盘（手）
    roe: float = 0.0  # ROE
    zgb: float = 0.0  # 总股本（股）
    ltgb: float = 0.0  # 流通股本（股）
    zys: float = 0.0  # 总营收（元）
    zystb: float = 0.0  # 总营收同比（%）
    jlr: float = 0.0  # 净利润
    mgwfplr: float = 0.0  # 每股未分配利润
    mlil: float = 0.0  # 毛利率
    fzl: float = 0.0  # 负债率
    mggjj: float = 0.0  # 每股公积金（元）
    zljlr: float = 0.0  # 今日主力净流入-净额（元）
    cddlr: float = 0.0  # 今日超大单流入（元）
    cddlc: float = 0.0  # 今日超大单流出（元）
    cddjlr: float = 0.0  # 今日超大单净流入-净额（元）
    z30: float = 0.0  # 今日超大单净流入-净占比（%）
    ddlr: float = 0.0  # 今日大单流入（元）
    ddlc: float = 0.0  # 今日大单流出（元）
    ddjlr: float = 0.0  # 今日大单净流入-净额（元）
    z33: float = 0.0  # 今日大单净流入-净占比（%）
    zdlr: float = 0.0  # 今日中单流入（元）
    zdlc: float = 0.0  # 今日中单流出（元）
    zdjlr: float = 0.0  # 今日中单净流入-净额（元）
    z36: float = 0.0  # 今日中单净流入-净占比（%）
    xdlr: float = 0.0  # 今日小单流入（元）
    xdlc: float = 0.0  # 今日小单流出（元）
    xdjlr: float = 0.0  # 今日小单净流入-净额（元）
    z39: float = 0.0  # 今日小单净流入-净占比（%）
    z50: str = '-'  # 归属行业板块名称
    z52: str = '-'  # 归属地域板块名称
    z53: str = '-'  # 归属概念板块名称
    zf05: float = 0.0  # 5日涨跌幅（%）
    zf20: float = 0.0  # 20日涨幅（%）
    mgsy: float = 0.0  # 每股收益（元）
    mgjzc: float = 0.0  # 每股净资产
    jsyl: float = 0.0  # 市盈率（静）
    ttmsyl: float = 0.0  # 市盈率（TTM）
    z71: float = 0.0  # 3日涨跌幅（%）
    jlil: float = 0.0  # 净利率
    jzc: float = 0.0  # 净资产
    zf10: float = 0.0  # 10日涨幅（%）
    z98: float = 0.0  # 5日主力净流入-净额（元）
    z99: float = 0.0  # 5日主力净流入-净占比（%）
    z100: float = 0.0  # 5日超大单净流入-净额（元）
    z101: float = 0.0  # 5日超大单净流入-净占比（%）
    z102: float = 0.0  # 5日大单净流入-净额（元）
    z103: float = 0.0  # 5日大单净流入-净占比（%）
    z104: float = 0.0  # 5日中单净流入-净额（元）
    z105: float = 0.0  # 5日中单净流入-净占比（%）
    z106: float = 0.0  # 5日小单净流入-净额（元）
    z107: float = 0.0  # 5日小单净流入-净占比（%）
    z108: float = 0.0  # 10日主力净流入-净额（元）
    z109: float = 0.0  # 10日主力净流入-净占比（%）
    z110: float = 0.0  # 10日超大单净流入-净额（元）
    z111: float = 0.0  # 10日超大单净流入-净占比（%）
    z112: float = 0.0  # 10日大单净流入-净额（元）
    z113: float = 0.0  # 10日大单净流入-净占比（%）
    z114: float = 0.0  # 10日中单净流入-净额（元）
    z115: float = 0.0  # 10日中单净流入-净占比（%）
    z116: float = 0.0  # 10日小单净流入-净额（元）
    z117: float = 0.0  # 10日小单净流入-净占比（%）
    z118: float = 0.0  # 今日主力净流入-净占比（%）
    z137: str = '-'  # 今日主力净流入最大股名称
    z138: str = '-'  # 今日主力净流入最大股代码
    z197: str = '-'  # 行业代码
    z199: float = 0.0  # 3日主力净流入-净额（元）
    z200: float = 0.0  # 3日主力净流入-净占比（%）
    z201: float = 0.0  # 3日超大单净流入-净额（元）
    z202: float = 0.0  # 3日超大单净流入-净占比（%）
    z203: float = 0.0  # 3日大单净流入-净额（元）
    z204: float = 0.0  # 3日大单净流入-净占比（%）
    z205: float = 0.0  # 3日中单净流入-净额（元）
    z206: float = 0.0  # 3日中单净流入-净占比（%）
    z207: float = 0.0  # 3日小单净流入-净额（元）
    z208: float = 0.0  # 3日小单净流入-净占比（%）
    ztj: float = 0.0  # 涨停价（元）
    dtj: float = 0.0  # 跌停价（元）
    jjia: float = 0.0  # 均价（元）


@dataclass
class WZWKMinuteDataItem(StockBaseItem):
    """分钟线数据信息"""

    code: str = '-'  # 股票代码
    tdate: str = '-'  # 分时时间
    open: float = 0.0  # 开盘价（成交均价）
    close: float = 0.0  # 收盘价
    high: float = 0.0  # 最高价
    low: float = 0.0  # 最低价
    cjl: float = 0.0  # 成交量（手）
    cje: float = 0.0  # 成交额（元）
    cjjj: float = 0.0  # 成交均价


@dataclass
class WZWKHourDataItem(StockBaseItem):
    """小时线数据信息"""

    code: str = '-'  # 股票代码
    name: str = '-'  # 股票名称
    ktype: int = 0  # K线类别
    tdate: str = '-'  # 交易时间
    open: float = 0.0  # 开盘价
    close: float = 0.0  # 收盘价
    high: float = 0.0  # 最高价
    low: float = 0.0  # 最低价
    cjl: float = 0.0  # 成交量
    cje: float = 0.0  # 成交额
    hsl: float = 0.0  # 换手率


@dataclass
class WZWKDayDataItem(StockBaseItem):
    """日线信息"""

    code: str = '-'  # 股票代码
    name: str = '-'  # 股票名称
    ktype: int = 0  # K线类别
    fq: int = 0  # 复权信息，除沪深京A股、B股、港股外，其余复权值默认为前复权
    tdate: str = '-'  # 交易时间
    open: float = 0.0  # 开盘价
    close: float = 0.0  # 收盘价
    high: float = 0.0  # 最高价
    low: float = 0.0  # 最低价
    cjl: float = 0.0  # 成交量
    cje: float = 0.0  # 成交额
    zf: float = 0.0  # 振幅
    zdf: float = 0.0  # 涨跌幅
    zde: float = 0.0  # 涨跌额
    hsl: float = 0.0  # 换手率


@dataclass
class WZWLevel2DataItem(StockBaseItem):
    """Level2 数据"""

    code: str = '-'  # 股票代码
    tdate: str = '-'  # 分时时间
    price: float = 0.0  # 成交价
    cjl: float = 0.0  # 成交量（手）
    trend: int = 0  # 相对于上个价位走势，1表示下跌或持平，2表示上涨或持平


@dataclass
class WZWBKDataItem(StockBaseItem):
    """板块成分股数据"""

    code: str = '-'  # 股票代码
    name: str = '-'  # 股票名称
    stype: int = 0  # 股票类型，1：深证股票，2：上证股票，3：北证股票，4：港股
    hsgt: int = 0  # 沪深港通，1：沪股通（港>沪）、2：深股通（港>深）、3：港股通（沪>港）、4：港股通（深>港）、5：港股通（深>港或沪>港）
    bk: str = '-'  # 所属板块，个股包括主板、创业板、科创板
    roe: float = 0.0  # OE
    zgb: float = 0.0  # 总股本（股）
    ltgb: float = 0.0  # 流通股本（股）
    ltsz: float = 0.0  # 流通市值（元）
    zsz: float = 0.0  # 总市值（元）
    ssdate: str = '-'  # 上市日期
    z50: str = '-'  # 归属行业板块名称
    z52: str = '-'  # 归属地域板块名称
    z53: str = '-'  # 归属概念板块名称


@dataclass
class WZWZSCSGDataItem(StockBaseItem):
    """指数成分股数据"""

    code: str = '-'  # 指数代码
    name: str = '-'  # 指数名称
    stockname: str = '-'  # 股票名称
    stockcode: str = '-'  # 股票代码
    weight: float = 0.0  # 成分股权重


@dataclass
class WZWZYZSCSGDataItem(StockBaseItem):
    """主要指数成分股数据"""

    mtype: int = 0  # 指数类别
    code: str = '-'  # 股票代码
    indexname: str = '-'  # 指数名称
    name: str = '-'  # 股票名称
    bps: float = 0.0  # 每股净资产（元）
    changerate: float = 0.0  # 涨跌幅
    closeprice: float = 0.0  # 最新价（元）
    eps: float = 0.0  # 每股收益（元）
    freecap: float = 0.0  # 流通市值（亿元）
    freeshares: float = 0.0  # 流通股本（亿股）
    industry: str = '-'  # 主营行业
    region: str = '-'  # 地区
    roe: float = 0.0  # 净资产收益率（%）
    secucode: str = '-'  # 股票安全代码
    totalshares: float = 0.0  # 总股本（亿股）
    weight: float = 0.0  # 成分股权重


@dataclass
class WZWSSHQDataItem(StockBaseItem):
    """实时行情数据"""
    code: str = '-'  # 股票代码
    name: str = '-'  # 股票名称
    zsz: float = 0.0  # 总市值（元）
    price: float = 0.0  # 最新价（元）
    zdfd: float = 0.0  # 涨跌幅度（%）
    zded: float = 0.0  # 涨跌额度（元）
    jjia: float = 0.0  # 均价（元）
    cjl: float = 0.0  # 成交量（手）
    cje: float = 0.0  # 成交额（元）
    lbi: float = 0.0  # 量比
    zhfu: float = 0.0  # 振幅（%）
    hslv: float = 0.0  # 换手率（%）
    high: float = 0.0  # 最高价（元）
    low: float = 0.0  # 最低价（元）
    open: float = 0.0  # 今日开盘价（元）
    zrspj: float = 0.0  # 昨日收盘价（元）
    z53: str = '-'  # 归属概念板块名称
    z50: str = '-'  # 归属行业板块名称
    z52: str = '-'  # 归属地域板块名称
    ztj: float = 0.0  # 涨停价（元）
    dtj: float = 0.0  # 跌停价（元）
    z118: float = 0.0  # 今日主力净流入-净占比（%）
    z71: float = 0.0  # 3日涨跌幅（%）
    zf05: float = 0.0  # 5日涨跌幅（%）
    zf10: float = 0.0  # 10日涨幅（%）
    zf20: float = 0.0  # 20日涨幅（%）
    zf60: float = 0.0  # 60日涨幅（%）
    zfy: float = 0.0  # 今年以来涨幅（%）
    dsyl: float = 0.0  # 市盈率（动态）
    ltsz: float = 0.0  # 流通市值（元）
    sjlv: float = 0.0  # 市净率（%）
    ssdate: str = '-'  # 上市日期
    weibi: float = 0.0  # 委比（%）
    wpan: float = 0.0  # 外盘（手）
    npan: float = 0.0  # 内盘（手）
    roe: float = 0.0  # ROE
    zgb: float = 0.0  # 总股本（股）
    ltgb: float = 0.0  # 流通股本（股）
    zys: float = 0.0  # 总营收（元）
    zystb: float = 0.0  # 总营收同比（%）
    jlr: float = 0.0  # 净利润
    mgwfplr: float = 0.0  # 每股未分配利润
    mlil: float = 0.0  # 毛利率
    fzl: float = 0.0  # 负债率
    mggjj: float = 0.0  # 每股公积金（元）
    zljlr: float = 0.0  # 今日主力净流入-净额（元）
    cddlr: float = 0.0  # 今日超大单流入（元）
    cddlc: float = 0.0  # 今日超大单流出（元）
    cddjlr: float = 0.0  # 今日超大单净流入-净额（元）
    z30: float = 0.0  # 今日超大单净流入-净占比（%）
    ddlr: float = 0.0  # 今日大单流入（元）
    ddlc: float = 0.0  # 今日大单流出（元）
    ddjlr: float = 0.0  # 今日大单净流入-净额（元）
    z33: float = 0.0  # 今日大单净流入-净占比（%）
    zdlr: float = 0.0  # 今日中单流入（元）
    zdlc: float = 0.0  # 今日中单流出（元）
    zdjlr: float = 0.0  # 今日中单净流入-净额（元）
    z36: float = 0.0  # 今日中单净流入-净占比（%）
    xdlr: float = 0.0  # 今日小单流入（元）
    xdlc: float = 0.0  # 今日小单流出（元）
    xdjlr: float = 0.0  # 今日小单净流入-净额（元）
    z39: float = 0.0  # 今日小单净流入-净占比（%）
    mgsy: float = 0.0  # 每股收益（元）
    mgjzc: float = 0.0  # 每股净资产
    jsyl: float = 0.0  # 市盈率（静）
    ttmsyl: float = 0.0  # 市盈率（TTM）
    jlil: float = 0.0  # 净利率
    jzc: float = 0.0  # 净资产
    z199: float = 0.0  # 3日主力净流入-净额（元）
    z200: float = 0.0  # 3日主力净流入-净占比（%）
    z201: float = 0.0  # 3日超大单净流入-净额（元）
    z202: float = 0.0  # 3日超大单净流入-净占比（%）
    z203: float = 0.0  # 3日大单净流入-净额（元）
    z204: float = 0.0  # 3日大单净流入-净占比（%）
    z205: float = 0.0  # 3日中单净流入-净额（元）
    z206: float = 0.0  # 3日中单净流入-净占比（%）
    z207: float = 0.0  # 3日小单净流入-净额（元）
    z208: float = 0.0  # 3日小单净流入-净占比（%）
    z98: float = 0.0  # 5日主力净流入-净额（元）
    z99: float = 0.0  # 5日主力净流入-净占比（%）
    z100: float = 0.0  # 5日超大单净流入-净额（元）
    z101: float = 0.0  # 5日超大单净流入-净占比（%）
    z102: float = 0.0  # 5日大单净流入-净额（元）
    z103: float = 0.0  # 5日大单净流入-净占比（%）
    z104: float = 0.0  # 5日中单净流入-净额（元）
    z105: float = 0.0  # 5日中单净流入-净占比（%）
    z106: float = 0.0  # 5日小单净流入-净额（元）
    z107: float = 0.0  # 5日小单净流入-净占比（%）
    z108: float = 0.0  # 10日主力净流入-净额（元）
    z109: float = 0.0  # 10日主力净流入-净占比（%）
    z110: float = 0.0  # 10日超大单净流入-净额（元）
    z111: float = 0.0  # 10日超大单净流入-净占比（%）
    z112: float = 0.0  # 10日大单净流入-净额（元）
    z113: float = 0.0  # 10日大单净流入-净占比（%）
    z114: float = 0.0  # 10日中单净流入-净额（元）
    z115: float = 0.0  # 10日中单净流入-净占比（%）
    z116: float = 0.0  # 10日小单净流入-净额（元）
    z117: float = 0.0  # 10日小单净流入-净占比（%）
    z137: str = '-'  # 今日主力净流入最大股名称
    z138: str = '-'  # 今日主力净流入最大股代码
    z197: str = '-'  # 行业代码
    tdate: str = '-'  # 交易时间
