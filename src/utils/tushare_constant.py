from src.utils.constant import WZW_NAME_TYPE
TUSHARE_TYPE_NAME = {
    "name"  : "股票名称",
    "ts_code":"股票代码",
    "date"  : "	交易日期",
    "time"  : "	交易时间",
    "open"  : "开盘价",
    "pre_close"  : "昨收价",
    "price"  : "现价",
    "high"  : "今日最高价",
    "low"  : "今日最低价",
    "bid"  : "竞买价，即“买一”报价（元）",
    "ask"  : "竞卖价，即“卖一”报价（元）",
    "volume":	"成交量（src=sina时是股，src=dc时是手）",
    "amount"  : "成交金额（元 CNY）",
    "b1_v"  : "委买一（量，单位：手，下同）",
    "b1_p"  : "委买一（价，单位：元，下同）",
    "b2_v"  : "委买二（量）",
    "b2_p"  : "委买二（价）",
    "b3_v"  : "委买三（量）",
    "b3_p"  : "委买三（价）",
    "b4_v"  : "委买四（量）",
    "b4_p"  : "委买四（价）",
    "b5_v"  : "委买五（量）",
    "b5_p"  : "委买五（价）",
    "a1_v"  : "委卖一（量，单位：手，下同）",
    "a1_p"  : "委卖一（价，单位：元，下同）",
    "a2_v"  : "委卖二（量）",
    "a2_p"  : "委卖二（价）",
    "a3_v"  : "委卖三（量）",
    "a3_p"  : "委卖三（价）",
    "a4_v"  : "委卖四（量）",
    "a4_p"  : "委卖四（价）",
    "a5_v"  : "委卖五（量）",
    "a5_p"  : "委卖五（价）",
    "trade_date": '交易日期',
    "p_change":'涨跌幅',
    "close":"收盘价",
    "change":"涨跌额",
    "atr21":'21日振幅',
    'atr14':"14日振幅",
    "pct_chg":"涨跌幅 （未复权，如果是复权请用 通用行情接口 )",
    "vol":"成交量 （手）",
    "turnover":"成交额",
    "turnover_rate":"换手率"
}

TUSHARE_TYPE_NAME.update(WZW_NAME_TYPE)