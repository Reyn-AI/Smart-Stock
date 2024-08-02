from src.utils.common import get_time

DEFAULT_PARAMS = [
    {   'name':'初始资金',
    'code':'cash',
    'default': 100000,
    'uiType':'input',
    'dtype':'float',
    'desc': '回测初始资金'
},
{   'name':'回测开始日期',
    'code':'start_date',
    'default': '2023-01-01',
    'uiType':'date',
    'desc':'回测开始日期'
},
{   'name':'回测结束日期',
    'code':'end_date',
    'default': get_time(template="%Y-%m-%d"),
    'uiType':'date',
    'desc': '回测结束日期'
},
 {
    'name':'手续费',
    'code':'commission',
    'default': 3/10000,
    'uiType':'input',
    'dtype': 'float',
    'desc':'券商手续费'
},
{   'name':'滑点率',
    'code':'slippage_perc',
    'default': 0.1/100,
    'uiType':'input',
    'dtype':'float',
    'desc': '由于网络原因导致买入卖出存在一定偏差，滑点率百分比。'
},
{
    'name':'最大成交量限制',
    'code':'size',
    'default': -1, 
    'uiType':'input',
    'dtype':'int',
    'desc': '-1表示无限制, 否则超出最大成交量部分不会被成交。'
},
{
    'name':'印花税',
    'code':'stamp_duty',
    'default': 2.5/10000, 
    'uiType':'input',
    'dtype':'int',
    'desc': '印花税默认万分之二点五'
},
{
    'name':'基线',
    'code':'benchmark',
    'default': '沪深300',
    'uiType':'input',
    'dtype':'string',
    'desc': '收益率对比基线，默认上证指数'
}
]
