"""常量"""
import os 

WZW_COMMON_STOCK_LIST_API = {
    "base_url": "http://api.waizaowang.com/doc/getBaseInfo",
    "params": ["type", "code", "fields", "export", "token", "filter"],
    "type": {
        "沪深京A股": 1,
        "沪深京B股": 2,
           '港股':3,
           '美股':4,
           '黄金':5,
           '汇率':6,
           'Reits':7,
           '沪深指数':10,
           '香港指数':11,
           '全球指数':12,
           '债券指数':13,
           '场内基金':20,
           '沪深债券':30,
           '行业板块':40,
           '概念板块':41,
           '地域板块':42
    },
}  # 股票列表

WZW_COMMON_CATEGORY_STOCK_LIST_API = {
    "base_url": "http://api.waizaowang.com/doc/getStockType",
    "params": ["flags", "fields", "export", "token", "filter"],
}  # 股票分类列表

WZW_COMMON_FUND_FLOW_API = {
    "base_url": "http://api.waizaowang.com/doc/getIndicatorBaseInfo",
    "params": [
        "type",
        "code",
        "startDate",
        "endDate",
        "fields",
        "export",
        "token",
        "filter",
    ],
}  # 资金流向

WZW_COMMON_Metric_API = {
    "base_url": "http://api.waizaowang.com/doc/getIndicatorMoney",
    "params": [
        "type",
        "code",
        "startDate",
        "endDate",
        "fields",
        "export",
        "token",
        "filter",
    ],
}  # 基本指标

WZW_COMMON_DAILY_QUOTATION_API = {
    "base_url": "http://api.waizaowang.com/doc/getDailyMarket",
    "params": [
        "type",
        "code",
        "startDate",
        "endDate",
        "fields",
        "export",
        "token",
        "filter",
    ],
}  # 每日行情

WZW_COMMON_K_MINUTE_DATA_API = {
    "base_url": "http://api.waizaowang.com/doc/getMinuteKLine",
    "params": [
        "type",
        "code",
        "startDate",
        "endDate",
        "fields",
        "export",
        "token",
        "filter",
    ],
}  # 分线数据

WZW_COMMON_K_HOUR_DATA_API = {
    "base_url": "http://api.waizaowang.com/doc/getMinuteKLine",
    "params": [
        "type",
        "code",
        "startDate",
        "endDate",
        "fields",
        "export",
        "token",
        "filter",
        "ktype",
    ],
}  # 时线数据

WZW_COMMON_K_DAY_DATA_API = {
    "base_url": "http://api.waizaowang.com/doc/getDayKLine",
    "params": [
        "type",
        "code",
        "startDate",
        "endDate",
        "fields",
        "export",
        "token",
        "filter",
        "ktype",
        "fq",
    ],
}  # 日线数据

WZW_COMMON_LEVEL2_DATA_API = {
    "base_url": "http://api.waizaowang.com/doc/getLevel2TimeDeal",
    "params": [
        "type",
        "code",
        "startDate",
        "endDate",
        "fields",
        "export",
        "token",
        "filter",
    ],
}  # Level2


WZW_CFG_BK_STOCKS_DATA_API = {
    "base_url": "http://api.waizaowang.com/doc/getHangyeCfg",
    "params": [
        "bkcode",
        "fields",
        "export",
        "token",
        "filter",
        "ktype",
        "fq",
    ],
}  # 板块成分股

WZW_CFG_ZS_STOCKS_DATA_API = {
    "base_url": "http://api.waizaowang.com/doc/getZhiShuChengFenGuZhongZhen",
    "params": [
        "code",
        "fields",
        "export",
        "token",
        "filter",
    ],
    "mtype":{
        1:'沪深300',
        2:'上证50',
        3:'中证500',
        4:'科创50'
    }
}  # 指数成分股

WZW_CFG_ZYZS_STOCKS_DATA_API = {
    "base_url": "http://api.waizaowang.com/doc/getZhiShuChengFenGu",
    "params": [
        "mtype",
        "fields",
        "export",
        "token",
        "filter",
    ],
}  # 主要指数成分股

WZW_SSHQ_STOCK_DATA_API = {
    "base_url": "http://api.waizaowang.com/doc/getWatchStockTimeKLine",
    "params": [
        "type",
        "code",
        "fields",
        "export",
        "token",
        "filter",
    ],
    "type": {
        "沪深京A股": 1,
        "沪深京B股": 2,
           '港股':3,
           '美股':4,
           '黄金':5,
           '汇率':6,
           'Reits':7,
           '沪深指数':10,
           '香港指数':11,
           '全球指数':12,
           '债券指数':13,
           '场内基金':20,
           '沪深债券':30,
           '行业板块':40,
           '概念板块':41,
           '地域板块':42
    },
}  # 实时行情

WZW_STOCK_TYPE = {
    1: "深证股票",
    2: "上证股票",
    3: "北证股票",
    4: "港股",
}

USER_TOKEN = os.getenv('WZW_TOKEN', "723af5665ef13aad9578f854229511ad")
TUSHARE_TOKEN = os.getenv('TUSHARE_TOKEN', '576fcd0631a5036932846f5f6de652dd2857aa38e62004cc1b53211a')

WZW_HSGT_TYPE = {
    0: "大陆",
    1: "沪股通（港>沪)",
    2: "深股通（港>深)",
    3: "港股通（沪>港)",
    4: "港股通（深>港)",
    5: "港股通（深>港或沪>港)",
}

WZW_NAME_TYPE = {
    "stype": "市场类型",
    "code": "股票代码",
    "name": "股票名称",
    "hsgt": "沪深港通",
    "bk": "板块",
    "roe": "净资产收益率",
    "zgb": "总股本",
    "ltgb": "流通股本",
    "ltsz": "流通市值",
    "zsz": "总市值",
    "ssdate": "上市时间",
    "z50": "行业板块",
    "z52": "地域板块",
    "z53": "概念",
    "tdate": "交易时间",
    "price": "最新价格(元)",
    "zdfd": "涨跌幅(%)",
    "zded": "涨跌额度(元)",
    "cjl": "成交量(手)",
    "cje": "成交额(元)",
    "zhfu": "振幅(%)",
    "hslv": "换手率(%)",
    "dsyl": "市盈率(动态)",
    "lbi": "量比",
    "high": "最高价",
    "low": "最低价",
    "open": "今日开盘价(元)",
    "zrspj": "昨日收盘价(元)",
    "sjlv": "市净率(%)",
    "zf60": "60日振幅(%)",
    "zfy": "今年以来涨幅(%)",
    "weibi": "委比(%)",
    "wpan": "外盘(手)",
    "npan": "内盘(手)",
    "zys": "总营收(元)",
    "zystb": "总营收同比(%)",
    "jlr": "净利润",
    "mgwfplr": "每股未分配利润",
    "mlil": "毛利率",
    "fzl": "负债率",
    "mggjj": "每股公积金(元)",
    "zljlr": "今日主力净流入-净额(元)",
    "cddlr": "今日超大单流入(元)",
    "cddlc": "今日超大单流出(元)",
    "cddjlr": "今日超大单净流入-净额(元)",
    "z30": "今日超大单净流入-净占比(%)",
    "ddlr": "今日大单流入(元)",
    "ddlc": "今日大单流出(元)",
    "ddjlr": "今日大单净流入-净额(元)",
    "z33": "今日大单净流入-净占比(%)",
    "zdlr": "今日中单流入(元)",
    "zdlc": "今日中单流出(元)",
    "zdjlr": "今日中单净流入-净额(元)",
    "z36": "今日中单净流入-净占比(%)",
    "xdlr": "今日小单流入(元)",
    "xdlc": "今日小单流出(元)",
    "xdjlr": "今日小单净流入-净额(元)",
    "z39": "今日小单净流入-净占比(%)",
    "zf05": "5日涨跌幅(%)",
    "zf20": "20日涨幅(%)",
    "mgsy": "每股收益(元)",
    "mgjzc": "每股净资产",
    "jsyl": "市盈率(净)",
    "ttmsyl": "市盈率(TTM)",
    "z71": "3日涨跌幅(%)",
    "jlil": "净利率",
    "jzc": "净资产",
    "zf10": "10日涨幅(%)",
    "z98": "5日主力流入-净额(元)",
    "z99": "5日主力净流入-净占比(%)",
    "z100": "5日超大单净流入-净额(元)",
    "z101": "5日超大单净流入-净占比(%)",
    "z102": "5日大单净流入-净额(元)",
    "z103": "5日大单净流入-净占比(%)",
    "z104": "5日中单净流入-净额(元)",
    "z105": "5日中单净流入-净占比(%)",
    "z106": "5日小单净流入-净额(元)",
    "z107": "5日小单净流入-净占比(%)",
    "z108": "10日主力净流入-净额(元)",
    "z109": "10日主力净流入-净占比(%)",
    "z110": "10日超大单净流入-净额（元",
    "z111": "10日超大单净流入-净占比（%)",
    "z112": "10日大单净流入-净额（元)",
    "z113": "10日大单净流入-净占比（%)",
    "z114": "10日中单净流入-净额（元)",
    "z115": "10日中单净流入-净占比（%)",
    "z116": "10日小单净流入-净额（元)",
    "z117": "10日小单净流入-净占比（%)",
    "z118": "今日主力净流入-净占比（%)",
    "z137": "今日主力净流入最大股名称",
    "z138": "今日主力净流入最大股代码",
    "z197": "行业代码",
    "z199": "3日主力净流入-净额（元)",
    "z200": "3日主力净流入-净占比（%)",
    "z201": "3日超大单净流入-净额（元)",
    "z202": " 3日超大单净流入-净占比（%)",
    "z203": "3日大单净流入-净额（元)",
    "z204": "3日大单净流入-净占比（%)",
    "z205": "3日中单净流入-净额（元)",
    "z206": "3日中单净流入-净占比（%)",
    "z207": "3日小单净流入-净额（元)",
    "z208": "3日小单净流入-净占比（%)",
    "ztj": "涨停价（元)",
    "dtj": "跌停价（元)",
    "jjia": "均价(元)",
    "close": "收盘价",
    "cjjj": "成交均价"
}

COMMON_API_TYPE = {
    'stock_list': '股票列表',
    'real_time_data':'当日实时数据',
    'minute_k_line': '分线数据',
    'hour_k_line': '时线数据',
    'day_k_line': '日线数据',
    'level2': 'level2数据',
    'block_data': '板块成分股',
    'exponent_data': '指数成分股',
    'major_exponent_data':'主要指数成分股',
    'history_real_time_data':'当日实时历史数据',
    'ths_special_data':"获取同花顺特色数据"}


MARKET_TYPE = {
    1: "深证股票",
    2: "上证股票",
    3: "北证股票",
    4: "创业板",
    5: "科创板",
    6: '科创50',
    7: '沪深300',
    8: '上证50',
    9: '中证1000'
}

BAO_STOCK_NAME = {
    'date':'日期',
    'preclose':'昨日收盘价',
    'adjustflag':'复权状态',
    'turn': '换手率',
    'tradestatus':'交易状态',
    'pctChg':'涨跌幅(%)',
    'peTTM': '滚动市盈率',
    'psTTM': '滚动市销率',
    'pcfNcfTTM': '滚动市现率',
    'pbMRQ': '市净率',
    'isST':'是否ST',
    'pubDate':'财报发布日期',
    'statDate': '统计截止日期',
    'roeAvg':'净资产收率(平均)(%)',
    'npMargin':'销售净利率(%)',
    'gpMargin':"销售毛利率(%)",
    'netProfit':"净利润(元)",
    'epsTTM':"每股收益",
    'MBRevenue':"主营营业收入(元)",
    'totalShare': "总股本",
    "liqaShare":"流通股本",
    'NRTurnRatio':"应收账款周转率(次)",
    "NRTurnDays": "应收账款周转天数(天)",
    "INVTurnRatio":"存货周转率(次)",
    "INVTurnDays":"存货周转天数(天)",
    "CATurnRatio": "流动资产周转率(次)",
    "AssetTurnRatio":"总资产周转率",
    "YOYEquity":"净资产同比增长率",
    "YOYAsset":"总资产同比增长率",
    "YOYNI":"净利润同比增长率",
    "YOYEPSBasic":"基本每股收益同比增长率",
    "YOYPNI":"归属母公司股东净利润同比增长率",
    "currentRatio":"流动比率",
    "quickRatio":"速率比率",
    "cashRatio":"现金比率",
    "YOYLiability":"总负债同比增长率",
    "liabilityToAsset":"资产负债率",
    "assetToEquity":"权益乘数",
    "CAToAsset":"流动资产除以总资产",
    "NCAToAsset":"非流动资产除以总资产",
    "tangibleAssetToAsset":"有形资产除以总资产",
    "ebitToInterest":"已获利息倍数",
    "CFOToOR":"经营活动产生的现金流量净额除以营业收入",
    "CFOToNP":"经营性现金净流量除以净利润",
    "CFOToGr":"经营性现金净流量除以营业总收入",
    "dupontROE":"净资产收益率",
    "dupontAssetStoEquity":"权益乘数(反映企业财务杠杆效应强弱和财务风险)",
    "dupontAssetTurn":"总资产周转率",
    "dupontPnitoni":"归属母公司股东的净利润/净利润",
    "dupontNitogr":"净利润/营业总收入",
    "dupontTaxBurden":"净利润/利润总额",
    "dupontIntburden":"利润总额/息税前利润",
    "dupontEbittogr":"息税前利润/营业总收入",
    "performanceExpPubDate":"业绩快报披露日",
    "performanceExpStatDate":"业绩快报统计日期",
    "performanceExpUpdateDate":"业绩快报披露日(最新)",
    "performanceExpressTotalAsset":"业绩快报总资产",
    "performanceExpressNetAsset":"业绩快报净资产",
    "performanceExpressEPSChgPct":"业绩每股收益增长率",
    "performanceExpressROEWa":"业绩快报净资产收益率ROE-加权",
    "performanceExpressEPSDiluted":"业绩快报每股收益EPS-摊薄",
    "performanceExpressGRYOY":"业绩快报营业总收入同比",
    "performanceExpressOPYOY":"业绩快报营业利润同比"
    
}
BAO_STOCK_NAME.update(WZW_NAME_TYPE)
BAO_STOCK_NAME = {k.lower():v for k,v in BAO_STOCK_NAME.items()}