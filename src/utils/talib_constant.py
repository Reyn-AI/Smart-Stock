"""talib api描述"""
#成交量指标
TALIB_DESC_VOLUME= [{
    'value':'AD',
    'label':'累积/派发线（Accumulation/Distribution Line）',
    'must_params': ['high', 'low', 'close', 'volume'],
    'desc':'Marc Chaikin提出的一种平衡交易量指标，以当日的收盘价位来估算成交流量，用于估定一段时间内该证券累积的资金流量。',
    'view':'subChart' #可视化的方式 'subChart|overlap|markPoint' 子图|k线重叠|k线标记
},
             {
    'value':'ADOSC',
    'label':'Chaikin A/D Oscillator Chaikin震荡指标',
    'must_params': ['high', 'low', 'close', 'volume'],
    'other_params': ['fastperiod=3', 'slowperiod=10'],
    'desc':'将资金流动情况与价格行为相对比，检测市场中资金流入和流出的情况。',
    'view': 'subChart'
},
             {
    'value':'OBV',
    'label':'On Balance Volume 能量潮',
    'must_params': ['close', 'volume'],
    'desc':'Joe Granville提出，通过统计成交量变动的趋势推测股价趋势。',
    'view': 'subChart'
},
             ]

TALIB_DESC_VOLUME_DICT = {x['value']:x for x in TALIB_DESC_VOLUME}
#图形模式
TALIB_DESC_PATTERN= [{
    'value':'CDL2CROWS',
    'label':'Two Crows 两只乌鸦',
    'must_params':['open', 'high', 'low', 'close'],
    'desc': '三日K线模式，第一天长阳，第二天高开收阴，第三天再次高开继续收阴，收盘比前一日收盘价低，预示股价下跌。'
},
             {
    'value':'CDL3BLACKCROWS',
    'label':'Three Black Crows 三只乌鸦',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，连续三根阴线，每日收盘价都下跌且接近最低价，每日开盘价都在上根K线实体内，预示股价下跌。'
},
             {
    'value':'CDL3INSIDE',
    'label':'Three Inside Up/Down 三内部上涨和下跌',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，母子信号+长K线，以三内部上涨为例，K线为阴阳阳，第三天收盘价高于第一天开盘价，第二天K线在第一天K线内部，预示着股价上涨。'
},
             {
    'value':'CDL3STARSINSOUTH',
    'label':'Three Stars In The South 南方三星',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，与大敌当前相反，三日K线皆阴，第一日有长下影线，第二日与第一日类似，K线整体小于第一日，第三日无下影线实体信号，成交价格都在第一日振幅之内，预示下跌趋势反转，股价上升。'
},
             {
    'value':'CDL3WHITESOLDIERS',
    'label':'红三兵',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，三日K线皆阳，每日收盘价变高且接近最高价，开盘价在前一日实体上半部，预示股价上升。'
},
{
    'value':'CDLABANDONEDBABY',
    'label':'Abandoned Baby 弃婴',
    'must_params':['open', 'high', 'low', 'close'],
    'other_params': ['penetration=0'],
    'desc':'三日K线模式，第二日价格跳空且收十字星（开盘价与收盘价接近，最高价最低价相差不大），预示趋势反转，发生在顶部下跌，底部上涨。'
},
{
    'value':'CDLADVANCEBLOCK',
    'label':'Advance Block 大敌当前',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，三日都收阳，每日收盘价都比前一日高，开盘价都在前一日实体以内，实体变短，上影线变长。'
},
{
    'value':'CDLBELTHOLD',
    'label':'Belt-hold 捉腰带线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'两日K线模式，下跌趋势中，第一日阴线，第二日开盘价为最低价，阳线，收盘价接近最高价，预示价格上涨。'
},
{
    'value':'CDLBREAKAWAY',
    'label':'Breakaway 脱离',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'五日K线模式，以看涨脱离为例，下跌趋势中，第一日长阴线，第二日跳空阴线，延续趋势开始震荡，第五日长阳线，收盘价在第一天收盘价与第二天开盘价之间，预示价格上涨。'
},
{
    'value':'CDLCLOSINGMARUBOZU',
    'label':'Closing Marubozu 收盘缺影线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，以阳线为例，最低价低于开盘价，收盘价等于最高价，预示着趋势持续。'
},
{
    'value':'CDLCONCEALBABYSWALL',
    'label':'Concealing Baby Swallow 藏婴吞没',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'四日K线模式，下跌趋势中，前两日阴线无影线，第二日开盘、收盘价皆低于第二日，第三日倒锤头，第四日开盘价高于前一日最高价，收盘价低于前一日最低价，预示着底部反转。'
},
{
    'value':'CDLCOUNTERATTACK',
    'label':'Counterattack 反击线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，与分离线类似。'
},
{
    'value':'CDLDARKCLOUDCOVER',
    'label':'Dark Cloud Cover 乌云压顶',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，第一日长阳，第二日开盘价高于前一日最高价，收盘价处于前一日实体中部以下，预示着股价下跌。'
},
{
    'value':'CDLDOJI',
    'label':'Doji 十字',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，开盘价与收盘价基本相同。'
},
{
    'value':'CDLDOJISTAR',
    'label':'Doji Star 十字星',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，开盘价与收盘价基本相同，上下影线不会很长，预示着当前趋势反转。'
},
{
    'value':'CDLDRAGONFLYDOJI',
    'label':'Dragonfly Doji 蜻蜓十字/T形十字',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，开盘后价格一路走低，之后收复，收盘价与开盘价相同，预示趋势反转。'
},
{
    'value':'CDLENGULFING',
    'label':'Engulfing Pattern 吞噬模式',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'两日K线模式，分多头吞噬和空头吞噬，以多头吞噬为例，第一日为阴线，第二日阳线，第一日的开盘价和收盘价在第二日开盘价收盘价之内，但不能完全相同。'
},
{
    'value':'CDLEVENINGDOJISTAR',
    'label':'Evening Doji Star 十字暮星',
    'must_params':['open', 'high', 'low', 'close'],
    'other_params':['penetration=0'],
    'desc':'三日K线模式，基本模式为暮星，第二日收盘价和开盘价相同，预示顶部反转。'
},
{
    'value':'CDLEVENINGSTAR',
    'label':'Evening Star 暮星',
    'must_params':['open', 'high', 'low', 'close'],
    'other_params':['penetration=0'],
    'desc':'三日K线模式，与晨星相反，上升趋势中，第一日阳线，第二日价格振幅较小，第三日阴线，预示顶部反转。'
},
{
    'value':'CDLGAPSIDESIDEWHITE',
    'label':'Up/Down-gap side-by-side white lines 向上/下跳空并列阳线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，上升趋势向上跳空，下跌趋势向下跳空，第一日与第二日有相同开盘价，实体长度差不多，则趋势持续。'
},
{
    'value':'CDLGRAVESTONEDOJI',
    'label':'Gravestone Doji 墓碑十字/倒T十字',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，开盘价与收盘价相同，上影线长，无下影线，预示底部反转。'
},
{
    'value':'CDLHAMMER',
    'label':'Hammer 锤头',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，实体较短，无上影线，下影线大于实体长度两倍，处于下跌趋势底部，预示反转。'
},
{
    'value':'CDLHANGINGMAN',
    'label':'Hanging Man 上吊线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，形状与锤子类似，处于上升趋势的顶部，预示着趋势反转。'
},
{
    'value':'CDLHARAMI',
    'label':'Harami Pattern 母子线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，分多头母子与空头母子，两者相反，以多头母子为例，在下跌趋势中，第一日K线长阴，第二日开盘价收盘价在第一日价格振幅之内，为阳线，预示趋势反转，股价上升。'
},
{
    'value':'CDLHARAMICROSS',
    'label':'Harami Cross Pattern 十字孕线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，与母子县类似，若第二日K线是十字线，便称为十字孕线，预示着趋势反转。'
},
{
    'value':'CDLHIGHWAVE',
    'label':'High-Wave Candle 风高浪大线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，具有极长的上/下影线与短的实体，预示着趋势反转。'
},
{
    'value':'CDLHIKKAKE',
    'label':'Hikkake Pattern 陷阱',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，与母子类似，第二日价格在前一日实体范围内，第三日收盘价高于前两日，反转失败，趋势继续。'
},
{
    'value':'CDLHIKKAKEMOD',
    'label':'Modified Hikkake Pattern 修正陷阱',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，与陷阱类似，上升趋势中，第三日跳空高开；下跌趋势中，第三日跳空低开，反转失败，趋势继续。'
},
{
    'value':'CDLHOMINGPIGEON',
    'label':'Homing Pigeon 家鸽',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，与母子线类似，不同的的是二日K线颜色相同，第二日最高价、最低价都在第一日实体之内，预示着趋势反转。'
},
{
    'value':'CDLIDENTICAL3CROWS',
    'label':'Identical Three Crows 三胞胎乌鸦',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，上涨趋势中，三日都为阴线，长度大致相等，每日开盘价等于前一日收盘价，收盘价接近当日最低价，预示价格下跌。'
},
{
    'value':'CDLINNECK',
    'label':'In-Neck Pattern 颈内线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，下跌趋势中，第一日长阴线，第二日开盘价较低，收盘价略高于第一日收盘价，阳线，实体较短，预示着下跌继续。'
},
{
    'value':'CDLINVERTEDHAMMER',
    'label':'Inverted Hammer 倒锤头',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，上影线较长，长度为实体2倍以上，无下影线，在下跌趋势底部，预示着趋势反转。'
},
{
    'value':'CDLKICKING',
    'label':'Kicking 反冲形态',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，与分离线类似，两日K线为秃线，颜色相反，存在跳空缺口。'
},
{
    'value':'CDLKICKINGBYLENGTH',
    'label':'较长缺影线决定的反冲形态',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，与反冲形态类似，较长缺影线决定价格的涨跌。'
},
{
    'value':'CDLLADDERBOTTOM',
    'label':'Ladder Bottom 梯底',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'五日K线模式，下跌趋势中，前三日阴线，开盘价与收盘价皆低于前一日开盘、收盘价，第四日倒锤头，第五日开盘价高于前一日开盘价，阳线，收盘价高于前几日价格振幅，预示着底部反转。'
},
{
    'value':'CDLLONGLEGGEDDOJI',
    'label':'Long Legged Doji 长脚十字',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，开盘价与收盘价相同居当日价格中部，上下影线长，表达市场不确定性。'
},
{
    'value':'CDLLONGLINE',
    'label':'Long Line Candle 长蜡烛',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，K线实体长，无上下影线。'
},
{
    'value':'CDLMARUBOZU',
    'label':'Marubozu 光头光脚/缺影线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，上下两头都没有影线的实体，阴线预示着熊市持续或者牛市反转，阳线相反。'
},
{
    'value':'CDLMATCHINGLOW',
    'label':'Matching Low 相同低价',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，下跌趋势中，第一日长阴线，第二日阴线，收盘价与前一日相同，预示底部确认，该价格为支撑位。'
},
{
    'value':'CDLMATHOLD',
    'label':'Mat Hold 铺垫',
    'must_params':['open', 'high', 'low', 'close'],
    'other_params':['penetration=0'],
    'desc':'五日K线模式，上涨趋势中，第一日阳线，第二日跳空高开影线，第三、四日短实体影线，第五日阳线，收盘价高于前四日，预示趋势持续。'
},
{
    'value':'CDLMORNINGDOJISTAR',
    'label':'Morning Doji Star 十字晨星',
    'must_params':['open', 'high', 'low', 'close'],
    'other_params':['penetration=0'],
    'desc':'三日K线模式，基本模式为晨星，第二日K线为十字星，预示底部反转。'
},
{
    'value':'CDLMORNINGSTAR',
    'label':'Morning Star 晨星',
    'must_params':['open', 'high', 'low', 'close'],
    'other_params':['penetration=0'],
    'desc':'三日K线模式，下跌趋势，第一日阴线，第二日价格振幅较小，第三天阳线，预示底部反转。'
},
{
    'value':'CDLONNECK',
    'label':'On-Neck Pattern 颈上线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，下跌趋势中，第一日长阴线，第二日开盘价较低，收盘价与前一日最低价相同，阳线，实体较短，预示着延续下跌趋势。'
},
{
    'value':'CDLPIERCING',
    'label':'Piercing Pattern 刺透形态',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'两日K线模式，下跌趋势中，第一日阴线，第二日收盘价低于前一日最低价，收盘价处在第一日实体上部，预示着底部反转。'
},
{
    'value':'CDLRICKSHAWMAN',
    'label':'Rickshaw Man 黄包车夫',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，与长腿十字线类似，若实体正好处于价格振幅中点，称为黄包车夫。'
},
{
    'value':'CDLRISEFALL3METHODS',
    'label':'Rising/Falling Three Methods 上升/下降三法',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'五日K线模式，以上升三法为例，上涨趋势中，第一日长阳线，中间三日价格在第一日范围内小幅震荡，第五日长阳线，收盘价高于第一日收盘价，预示股价上升。'
},
{
    'value':'CDLSEPARATINGLINES',
    'label':'Separating Lines 分离线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，上涨趋势中，第一日阴线，第二日阳线，第二日开盘价与第一日相同且为最低价，预示着趋势继续。'
},
{
    'value':'CDLSHOOTINGSTAR',
    'label':'Shooting Star 射击之星',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，上影线至少为实体长度两倍，没有下影线，预示着股价下跌'
},
{
    'value':'CDLSPINNINGTOP',
    'label':'Spinning Top 纺锤',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线，实体小。'
},
{
    'value':'CDLSTALLEDPATTERN',
    'label':'Stalled Pattern 停顿形态',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，上涨趋势中，第二日长阳线，第三日开盘于前一日收盘价附近，短阳线，预示着上涨结束。'
},
{
    'value':'CDLSTICKSANDWICH',
    'label':'Stick Sandwich 条形三明治',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，第一日长阴线，第二日阳线，开盘价高于前一日收盘价，第三日开盘价高于前两日最高价，收盘价于第一日收盘价相同。'
},
{
    'value':'CDLTAKURI',
    'label':'探水竿',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'一日K线模式，大致与蜻蜓十字相同，下影线长度长。'
},
{
    'value':'CDLTASUKIGAP',
    'label':'Tasuki Gap 跳空并列阴阳线',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，分上涨和下跌，以上升为例，前两日阳线，第二日跳空，第三日阴线，收盘价于缺口中，上升趋势持续。'
},
{
    'value':'CDLTHRUSTING',
    'label':'Thrusting Pattern 插入',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'二日K线模式，与颈上线类似，下跌趋势中，第一日长阴线，第二日开盘价跳空，收盘价略低于前一日实体中部，与颈上线相比实体较长，预示着趋势持续。'
},
{
    'value':'CDLTRISTAR',
    'label':'Tristar Pattern 三星',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，由三个十字组成，第二日十字必须高于或者低于第一日和第三日，预示着反转。'
},
{
    'value':'CDLUNIQUE3RIVER',
    'label':'Unique 3 River 奇特三河床',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，下跌趋势中，第一日长阴线，第二日为锤头，最低价创新低，第三日开盘价低于第二日收盘价，收阳线，收盘价不高于第二日收盘价，预示着反转，第二日下影线越长可能性越大。'
},
{
    'value':'CDLUPSIDEGAP2CROWS',
    'label':'向上跳空的两只乌鸦',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'三日K线模式，第一日阳线，第二日跳空以高于第一日最高价开盘，收阴线，第三日开盘价高于第二日，收阴线，与第一日比仍有缺口。'
},
{
    'value':'CDLXSIDEGAP3METHODS',
    'label':'上升/下降跳空三法',
    'must_params':['open', 'high', 'low', 'close'],
    'desc':'五日K线模式，以上升跳空三法为例，上涨趋势中，第一日长阳线，第二日短阳线，第三日跳空阳线，第四日阴线，开盘价与收盘价于前两日实体内，第五日长阳线，收盘价高于第一日收盘价，预示股价上升。'
}]

for item in TALIB_DESC_PATTERN:
    item['view'] = 'markPoint'  #以标签形式显示

TALIB_DESC_PATTERN_DICT= {x['value']:x for x in TALIB_DESC_PATTERN}

#交叉分析
TALIB_DESC_OVERLAP = [{
    'value':'BBANDS',
    'label':'布林线',
    'must_params':['close'],
    'other_params':['matype=1', 'timeperiod=5'],
    'desc':'利用统计原理，求出股价的标准差及其信赖区间，从而确定股价的波动范围及未来走势，利用波带显示股价的安全高低价位。',
    'view':'overlap',
    'return':['upper', 'middle', 'lower']
},
{
    'value':'KAMA',
    'label':'考夫曼的自适应移动平均线',
    'must_params':['close'],
    'other_params':['timeperiod = 30'],
    'desc':'一种高级均线算法，能根据价格曲线噪声的大小自动确定计算价格均线时的衰减系数。',
    'view':'overlap'
},
{
    'value':'MIDPRICE',
    'label':'阶段中点价格',
    'must_params':['close'],
    'other_params':['timeperiod=14'],
    'desc':'阶段中点价格',
    'view':'overlap'
},
{
    'value':'SAR',
    'label':'抛物线指标',
    'must_params':['high', 'low'],
    'other_params':['acceleration=0', 'maximum=0'],
    'desc':'抛物线转向也称停损点转向，是利用抛物线方式，随时调整停损点位置以观察买卖点。由于停损点（又称转向点SAR）以弧形的方式移动，故称之为抛物线转向指标 。',
    'view':'overlap'
},
{
    'value':'T3',
    'label':'三重移动平均线',
    'must_params':['close'],
    'other_params':['timeperiod=5', 'vfactor=0'],
    'desc':'T3是一种三重指数移动平均线，它通过对价格进行三次平滑来消除价格波动的噪音。T3可以更快地反应价格趋势的变化，因此在短期交易中比较常用。',
    'view':'overlap'
},
{
    'value':'TEMA                 ',
    'label':'三重指数移动平均线',
    'must_params':['close'],
    'other_params':['timeperiod=5'],
    'desc':'TEMA是一种三重指数移动平均线，它通过对价格进行三次平滑来消除价格波动的噪音。TEMA可以更快地反应价格趋势的变化，因此在短期交易中比较常用。',
    'view':'overlap'
}
]
TALIB_DESC_OVERLAP_DICT= {x['value']:x for x in TALIB_DESC_OVERLAP}

#波动指标
TALIB_DESC_VOLATILITY  = [{
    'value':'ATR',
    'label':'真实波动幅度均值',
    'must_params':['high', 'low', 'close'],
    'other_params':['timeperiod=14'],
    'desc':'可以显示资产价格波动的幅度',
    'view':'overlap'
},
{
    'value':'NATR',
    'label':'归一化波动幅度均值',
    'must_params':['high', 'low', 'close'],
    'other_params':['timeperiod=14'],
    'desc':'NATR指标是一种归一化的ATR指标，可以显示资产价格波动的幅度。',
    'view':'overlap'
},
{
    'value':'TRANGE',
    'label':'真正范围',
    'must_params':['high', 'low', 'close'],
    'desc':'RANGE指标是一种价格波动指标，可以显示资产价格波动的幅度。TRANGE指标通过计算当日的最高价与最低价之间的波动幅度，以及当日的收盘价与前一日收盘价之间的波动幅度，可以确定资产价格波动的幅度。',
    'view':'overlap'
}                          
]
TALIB_DESC_VOLATILITY_DICT= {x['value']:x for x in TALIB_DESC_VOLATILITY}

#动量指标
TALIB_DESC_MOMENTUM = [
    {
    'value':'ADX',
    'label':'平均趋向指数',
    'must_params':['high', 'low', 'close'],
    'other_params':['timeperiod=14'],
    'desc':'用于判断价格的趋势强度。',
    'view':'overlap'
},
     {
    'value':'ADXR',
    'label':'平均趋向指数的趋向指数',
    'must_params':['high', 'low', 'close'],
    'other_params':['timeperiod=14'],
    'desc':'ADXR是ADX的平均值，用于平滑ADX的波动。ADXR通常用于识别价格的长期趋势。',
    'view':'overlap'
},
  {
    'value':'APO',
    'label':'价格震荡指数',
    'must_params':['high', 'low', 'close'],
    'other_params':['slowperiod=26', 'matype=0'],
    'desc':'一种价格振荡指标，用于测量价格的变化幅度。APO通过计算两个移动平均线之间的差异来显示价格的变化幅度。',
    'view':'overlap'
},   
   {
    'value':'Aroon',
    'label':'阿隆指标',
    'must_params':['high', 'low'],
    'other_params':['timeperiod=14'],
    'desc':'一种价格趋势指标，用于识别价格是否处于上升或下降趋势中。Aroon通过计算最近一段时间内价格的最高值和最低值来显示价格的趋势。',
    'view':'overlap'
}, 
   {
    'value':'BOP',
    'label':'均势指标',
    'must_params':['open', 'high', 'low', 'close'],
    'other_params':['timeperiod=14'],
    'desc':'一种价格指标，用于测量买卖双方的力量。BOP通过计算当前价格与前一天收盘价之间的差异来显示买卖双方的力量。',
    'view':'overlap'
}, 
    {
    'value':'MFI',
    'label':'资金流量指标',
    'must_params':['high', 'low', 'close', 'volume'],
    'other_params':['timeperiod=14'],
    'desc':'一种成交量指标，用于测量资金流入和流出的力量。MFI通过计算成交量和价格之间的关系来显示资金的流入和流出。',
    'view':'overlap'
}, 
    {
    'value':'MINUS_DI',
    'label':'负方向指标',
    'must_params':['high', 'low', 'close'],
    'other_params':['timeperiod=14'],
    'desc':'一种趋势指标，用于显示价格趋势的强度。MINUS_DI通过计算负向运动指标（-DI）之间的差异来计算趋势强度。',
    'view':'overlap'
},
    {
    'value':'MINUS_DM',
    'label':'上升动向值',
    'must_params':['high', 'low', 'close'],
    'other_params':['timeperiod=14'],
    'desc':'一种趋势指标，用于显示价格趋势的强度。MINUS_DM通过计算前一天最高价与今天最高价之间的差异来计算下降趋势的强度。',
    'view':'overlap'
}
]
TALIB_DESC_MOMENTUM_DICT= {x['value']:x for x in TALIB_DESC_MOMENTUM}

#周期指标
TALIB_DESC_CYCLE = [
    {
    'value':'HT_DCPERIOD',
    'label':'希尔伯特变换-主导周期',
    'must_params':['close'],
    'desc':'一种周期指标，可以显示资产价格的周期性变化。HT_DCPERIOD指标通过对价格波动进行适当的滤波和处理，可以帮助识别资产价格的周期性变化，以及预测价格趋势。',
    'view':'overlap'
},
{
    'value':'HT_DCPHASE',
    'label':'希尔伯特变换-主导周期',
    'must_params':['close'],
    'desc':'一种相位指标，可以显示资产价格周期变化的相位差异。HT_DCPHASE指标可以帮助确定资产价格的周期性变化，以及价格趋势的方向和强度。',
    'view':'overlap'
},
{
    'value':'HT_PHASOR',
    'label':'希尔伯特变换-希尔伯特变换相量分量',
    'must_params':['close'],
    'desc':'一种相位指标，可以显示资产价格的相位和幅度。HT_PHASOR指标通过将价格波动分解为正弦和余弦波，可以帮助确定价格的周期性变化和价格趋势的方向。',
    'view':'overlap',
    'return': ['inphase', 'quadrature ']
},
{
    'value':'HT_SINE',
    'label':'希尔伯特变换-正弦波',
    'must_params':['close'],
    'desc':'一种周期指标，可以显示资产价格的周期性变化。HT_SINE指标通过对价格波动进行适当的滤波和处理，可以帮助识别资产价格的周期性变化，以及预测价格趋势。',
    'view':'overlap',
    'return': ['sine', 'leadsine  ']
},
{
    'value':'HT_TRENDMODE',
    'label':'希尔伯特变换-趋势与周期模式',
    'must_params':['close'],
    'desc':'一种趋势指标，可以显示资产价格趋势的方向和强度。HT_TRENDMODE指标通过将价格波动分解为趋势和周期成分，可以帮助确定价格趋势的方向和强度。',
    'view':'overlap'
},
]
TALIB_DESC_CYCLE_DICT= {x['value']:x for x in TALIB_DESC_CYCLE}

#统计指标
TABLE_DESC_STATISTIC = [
    {
    'value':'BETA ',
    'label':'贝塔系数',
    'must_params':['high', 'low'],
    'other_params':['timeperiod=5'],
    'desc':' β 越高，意味着股票相对于业绩评价基准的波动性越大。 β 大于 1 ，则股票的波动性大于业绩评价基准的波动性。反之亦然。',
    'view':'subChart' #可视化的方式 'subChart|overlap|markPoint' 子图|k线重叠|k线标记
},
{
    'value':'STDDEV',
    'label':'标准偏差',
    'must_params':['close'],
    'other_params':['timeperiod=5', 'nbdev=1'],
    'desc':'标准偏差越小，这些值偏离平均值就越少，反之亦然。标准偏差的大小可通过标准偏差与平均值的倍率关系来衡量。',
    'view':'subChart',
},
{
    'value':'TSF',
    'label':'时间序列预测',
    'must_params':['close'],
    'other_params':['timeperiod=14'],
    'desc':'一种历史资料延伸预测，也称历史引伸预测法。是以时间数列所能反映的社会经济现象的发展过程和规律性，进行引伸外推，预测其发展趋势的方法',
    'view':'subChart',
},
{
    'value':'VAR',
    'label':'方差',
    'must_params':['close'],
    'other_params':['timeperiod=5', 'nbdev=1'],
    'desc':'方差用来计算每一个变量（观察值）与总体均数之间的差异。',
    'view':'subChart',
},

]
TABLE_DESC_STATISTIC_DICT= {x['value']:x for x in TABLE_DESC_STATISTIC}