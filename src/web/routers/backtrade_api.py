from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from src.utils.common import *
from src.utils.stock_utils import *  
from src.utils.talib_constant import *
from src.utils.backtrader_constant import *
from src.web.utils.web_socket_utils import ConnectionManager
from src.backtest.backtrader_engine import BackTraderEngine
from src.backtest.backtrade_params import BackTraderParams, OrderParams, BrokerParams
from src.backtest.strategys.strategy_engine import StrategyEngine
from multiprocessing import Queue
import multiprocessing
from functools import partial
import json
from src.database.mongodb_utils import MongoDBUtil
from src.utils.registy import *
from functools import partial
from src.backtest.strategys.size_strategy import *
import numpy as np

router = APIRouter()

manager = ConnectionManager()

@router.post('/backtrade/get_default_params')
async def get_backer_trade_default_params():
    """获取backtrade默认参数"""
    res = {'code':200, 'msg':'', 'data':DEFAULT_PARAMS}
    return res


class BackTraderRecordItem(BaseModel):
    userID:str #用户id
    logQueen:List #日志信息
    recordName:str #保存的记录名
    cash:List #现金信息
    code:str #回测股票代码
    defaultParams:List #参数配置
    dayReturns: List #日收益率
    benchmark:List #基准收益率
    totalAssets:List #总资产
    dayKLine:Dict #日线信息
    returnsTable:List #指标信息列表
    orderInfos:Dict #买卖执行信息
    orderStockNames:List #回测买卖的股票池
    buyStrategys:List #买入策略信息
    sellStrategys:List #卖出策略信息
    buySizeStrategys:Dict = None #买入仓位管理策略
    sellSizeStrategys:Dict = None #卖出仓位管理策略
    buyCombineType:Dict = None #买入策略组合方式
    sellCombineType:Dict = None #卖出策略组合方式
    
class GetRecordItem(BaseModel):
    userID:str
    id:str = None

@router.post('/backtrade/save_record')
async def save_backtrader_record(params:BackTraderRecordItem):
    """保存回测记录"""
    res = {'code':200, 'msg':'保存成功', 'status':1}
    try:
        now = get_time('%Y-%m-%d %H:%M:%S')
        mogon = MongoDBUtil()
        data = {'userID':params.userID,
                'datetime':now,
                'logQueen':params.logQueen,
                'cash':params.cash,
                'code':params.code,
                'recordName':params.recordName,
                'defaultParams':params.defaultParams,
                'dayReturns':params.dayReturns,
                'benchmark':params.benchmark,
                'totalAssets':params.totalAssets,
                'dayKLine':params.dayKLine,
                'returnsTable':params.returnsTable,
                'orderInfos':params.orderInfos,
                'orderStockNames':params.orderStockNames,
                'buyStrategys':params.buyStrategys,
                'sellStrategys':params.sellStrategys,
                'buyCombineType':params.buyCombineType,
                'sellCombineType':params.sellCombineType,
                'buySizeStrategys':params.buySizeStrategys,
                'sellSizeStrategys':params.sellSizeStrategys}
        mogon.insert_backtrader_record(data)
    except Exception as e:
        res['code'] = 500
        res['status'] = 0
        res['msg'] = str(e)
    finally:
        return res

@router.post('/backtrade/delete_record_by_id')
async def delete_backtrader_record_by_id(params:GetRecordItem):
    """根据id删除记录"""
    res = {'code':200, 'msg':'操作成功', 'status':1}
    try:
        mogon = MongoDBUtil()
        mogon.delete_backtrader_record(id=params.id)
    except Exception as e:
        res['code'] = 500
        res['status'] = 0
        res['msg'] = str(e)
    finally:
        return res

@router.post('/backtrade/get_record_list')
async def get_backtrader_record_list(params:GetRecordItem):
    """获取回测记录"""
    res = {'code':200, 'msg':'请求成功', 'status':1, 'data':[], 'colNames':[], 'rawData':{}}
    try:
        mogon = MongoDBUtil()
        data = mogon.get_backtrader_record_data(user_id=params.userID) #{'_id', 'datetime', 'recordName', 'returnTable':[{'name', 'value'}]}
        res['rawData'] = {x['_id']:x for x in data}
        data_ = []
        for x in data:
            item = {}
            item['id'] = x['_id']
            item['回测日期'] = x['datetime']
            item['策略名'] = x['recordName']
            item['股票池'] = x['orderStockNames']
            for ret in x['returnsTable']:
                item[ret['name']] = ret['value']
            item['买入策略'] = [x['name'] for x in x['buyStrategys']]
            item['卖出策略'] = [x['name'] for x in x['sellStrategys']]
            item['买入仓位策略'] = x['buySizeStrategys']['name']
            item['卖出仓位策略'] = x['sellSizeStrategys']['name']
            item['买入策略组合方式'] = x['buyCombineType']['name']
            item['卖出策略组合方式'] = x['sellCombineType']['name']
            data_.append(item)
        res['data'] = data_
        if len(data_)>0:
            colNames = list(data_[0].keys())
            colNames.pop(0) #去掉id
            res['colNames'] = colNames
            
    except Exception as e:
        res['code'] = 500
        res['status'] = 0
        res['msg'] = str(e)
    finally:
        return res

@router.post('/backtrade/get_record_by_id')
async def save_backtrader_record(params:GetRecordItem):
    """获取单条详细回测记录"""
    res = {'code':200, 'msg':'', 'status':1, 'data':[]}
    try:
        mogon = MongoDBUtil()
        data = mogon.get_backtrader_record_data_by_id(id=params.id)
        res['data'] = data
    except Exception as e:
        res['code'] = 500
        res['status'] = 0
        res['msg'] = str(e)
    finally:
        return res

@router.post('/backtrade/get_strategys')
async def get_strategys():
    """获取策略列表"""
    res = {'code':200, 'msg':'', 'status':1, 'buyStrategys':[], 'sellStrategys':[], 'buyCombineType':[{'name':'条件同时满足', 'default':'and', 'desc':'所有策略都符合时才买入'},
                                                                                                      {'name':'其中一个条件满足即可', 'default':'or', 'desc':'所有策略有一个满足时就买入'}],
           'sellCombineType':[{'name':'条件同时满足', 'default':'and', 'desc':'所有策略都符合时才买入'},
                                                                                                      {'name':'其中一个条件满足即可', 'default':'or', 'desc':'所有策略有一个满足时就买入'}]}
    try:
        buy_strategys = get_buy_factor_registry()
        buy_strategys.extend(get_dynamic_buy_factor_registry())
        sell_strategys = get_sell_factor_registry()
        sell_strategys.extend(get_dynamic_sell_factor_registry())
        res['buyStrategys'] = buy_strategys
        res['sellStrategys'] = sell_strategys
    except Exception as e:
        res['code'] = 500
        res['status'] = 0
        res['msg'] = str(e)
    finally:
        return res

@router.post('/backtrade/get_size_strategys')
async def get_size_strategys():
    """获取仓位管理策略列表和结合方式"""
    res = {'code':200, 'msg':'', 'status':1, 'buySizeStrategys':[], 'sellSizeStrategys':[]}
    try:
        res['buySizeStrategys'] = get_buy_size_registry()
        res['sellSizeStrategys'] =  get_sell_size_registry()
        
    except Exception as e:
        res['code'] = 500
        res['status'] = 0
        res['msg'] = str(e)
    finally:
        return res


def gen_strategy_by_params(buy_params: list,
                           sell_params:list,
                           buy_size:dict=None,
                           sell_size:dict=None,
                           buy_combin_type:str='and',
                           sell_combin_type:str='and'):
    """根据传入的策略参数生成策略"""
    #先分类动态策略和静态策略
    buy_strategy = [] #静态买策略
    sell_strategy = [] #静态卖策略
    dynamic_buy_strategy = [] #动态买策略
    dynamic_sell_strategy = [] #动态卖策略
    dyn_buy_names = [x['code'] for x in DYNAMIC_BUY_FACTOR_REGISTRY]
    buy_names = [x['code'] for x in BUY_FACTOR_REGISTRY]
    dyn_sell_names = [x['code'] for x in DYNAMIC_SELL_FACTOR_REGISTRY]
    sell_names = [x['code'] for x in SELL_FACTOR_REGISTRY]
    for params in buy_params:
        if params['code'] in dyn_buy_names:
            dynamic_buy_strategy.append(params)
        elif params['code'] in buy_names:
            buy_strategy.append(params)
    for params in sell_params:
        if params['code'] in dyn_sell_names:
            dynamic_sell_strategy.append(params)
        elif params['code'] in sell_names:
            sell_strategy.append(params)
    if buy_size is None:
        buy_size_strategy = AllInStrategy()
    else:
        cls_name = buy_size.get('code')
        params  = buy_size.get('params', [])
        buy_size_strategy = eval(f'{cls_name}(params={params})')
    if sell_size is None:
        sell_size_strategy = AllInStrategy()
    else:
        cls_name = sell_size.get('code')
        params  = sell_size.get('params', [])
        sell_size_strategy = eval(f'{cls_name}(params={params})')
        
    strategy = partial(StrategyEngine,buy_singals=buy_strategy,
                              sell_singals=sell_strategy,
                              dynamic_buy_singals=dynamic_buy_strategy,
                              dynamic_sell_singals=dynamic_sell_strategy,
                              buy_combin_type=buy_combin_type,
                              sell_combin_type=sell_combin_type,
                              buy_size_strategy=buy_size_strategy,
                              sell_size_strategy=sell_size_strategy
                              )
    return strategy


@router.websocket('/backtrade/start/')
async def backtrade_start(websocket:WebSocket):
    """开始回测"""
    await manager.connect(websocket)
    try:
        r_params = await websocket.receive_text()
        r_params = eval(r_params)
        params = r_params['params'] #默认参数
        params = {x['code']:x['default'] for x in params}
        code = r_params['code'] #回测股票代码
        code = code.replace('，', ',')
        codes = code.split(',')
        if len(codes)==0:
            manager.send_personal_message(json.dumps({'type':'end'}, ensure_ascii=False), websocket) #结束符
        buy_strategys = r_params.get('buyStrategys', [])
        sell_strategys = r_params.get('sellStrategys', [])
        buy_size_strategy = r_params.get('buySizeStrategy')
        sell_size_strategy = r_params.get('sellSizeStrategy')
        buyCombineType = r_params.get('buyCombineType', {'default':'and'})
        sellCombineType = r_params.get('sellCombineType', {'default':'and'})
        if len(buy_strategys)==0 and len(sell_strategys)==0:
             manager.send_personal_message(json.dumps({'type':'error', 'data':'买卖策略不能为空!'}, ensure_ascii=False), websocket)
             manager.send_personal_message(json.dumps({'type':'end'}, ensure_ascii=False), websocket) #结束符
             return
        
        broker_params = BrokerParams(commission=params.get('commission', 3/10000),
                                     slippage_perc=params.get('slippage_perc', 1/1000),
                                     size=params.get('size'))
        backtrader_params = BackTraderParams(start_date=params.get('start_date', '2023-01-01'),
                         end_date=params.get('end_date', '2024-01-01'),
                         benchmark=params.get('benchmark'),
                         cash=params.get('cash'),
                         stamp_duty=params.get('stamp_duty'),
                         stock_list=codes,
                         msg_queen=Queue(100)
                         )
        backtrader_params.broker_params = broker_params
        strategy=gen_strategy_by_params(buy_params=buy_strategys,
                                        sell_params=sell_strategys,
                                        buy_size=buy_size_strategy,
                                        sell_size=sell_size_strategy,
                                        buy_combin_type=buyCombineType.get('default'),
                                        sell_combin_type=sellCombineType.get('default'))
        engine = BackTraderEngine(params=backtrader_params, strategy=strategy)
        p = multiprocessing.Process(target=partial(engine_run, engine=engine))
        p.start()
        cash_list = [] #现金曲线
        total_assets = [] #总资产曲线
        order_infos = {} #买卖点信息
        pnl_infos = {} #盈亏数据
        while True and engine.params.msg_queen is not None:
            time.sleep(0.001)
            if not engine.params.msg_queen.empty():
                msg = engine.params.msg_queen.get()
                if msg is None:
                    break
                # elif msg['type'] == 'benchmark':
                #     benchmark_data.append(round(msg['value']*100, 2)) #基准收益
                elif msg['type'] == 'broker_cash':
                    cash_list.append(msg['value'])
                elif msg['type'] == 'broker_sum':
                    total_assets.append(msg['value'])
                elif msg['type'] == 'order':
                    name = msg['data']['name']
                    order_type = msg['data']['type']
                    if name in order_infos.keys():
                        order_infos[name][order_type].append(msg['data'])
                    else:
                        order_infos[name] = {'sell':[], 'buy':[]}
                        order_infos[name][order_type].append(msg['data'])
                elif msg['type'] == 'pnl':
                    #计算胜率、平均盈亏、赔率
                    code = msg['data']['code'] #股票代码
                    pnl = msg['data']['pnl']
                    if code not in pnl_infos.keys():
                        pnl_infos[code] = {}
                        pnl_infos[code]['win'] = []
                        pnl_infos[code]['loss'] = []
                    if pnl>0:
                        pnl_infos[code]['win'].append(pnl)
                    else:
                        pnl_infos[code]['loss'].append(pnl)
                else:
                    await manager.send_personal_message(json.dumps(msg, ensure_ascii=False), websocket) #发送日志信息
        # 等待进程结束
        p.join()
        #处理收益率
        metrics_res = None
        if not engine.params.msg_queen.empty():
            metrics_res = engine.params.msg_queen.get()
        if len(pnl_infos)>0:
            mean_loss = np.array([x.get('loss') for x in pnl_infos.values()]).flatten()#平均亏损
            mean_loss = 0 if len(mean_loss)==0 else float(mean_loss.mean())
            mean_win = np.array([x.get('win', []) for x in pnl_infos.values()]).flatten() #平均收益
            mean_win = 0 if len(mean_win)==0 else float(mean_win.mean())
            win_ratio = float(np.array([len(x.get('win', []))/(len(x.get('win')) + len(x.get('loss'))) for x in pnl_infos.values()]).flatten().mean())
            trade_count = float(np.array([(len(x.get('win')) + len(x.get('loss'))) for x in pnl_infos.values()]).flatten().mean())
            pnlInfos = {'type':'msg', 'data':f"交易次数:{trade_count},交易胜率:{win_ratio*100}%, 平均亏损:{mean_loss}, 平均盈利:{mean_win}"}
            await manager.send_personal_message(json.dumps(pnlInfos, ensure_ascii=False), websocket)
            if metrics_res is not None:
                metrics_res['data'].append({'name':'交易胜率', 'value':f"{pnlInfos['data']}", 'type':'table'})
        await manager.send_personal_message(json.dumps(metrics_res, ensure_ascii=False), websocket) #发送metric指标
        plot_res = {'type':'plot',
                    'cash':list_nan_to_none(cash_list),
                    'totalAssets':list_nan_to_none(total_assets),
                    'orderInfos':order_infos,
                    'orderStockNames':list(order_infos.keys())}
        await manager.send_personal_message(json.dumps(plot_res, ensure_ascii=False), websocket)
        await manager.send_personal_message(json.dumps({'type':'end'}, ensure_ascii=False), websocket) #结束符
    except Exception as e:
        get_logger().error(str(e))
        manager.send_personal_message(json.dumps({'type':'end'}, ensure_ascii=False), websocket) #结束符
        manager.disconnect(websocket)

def engine_run(engine: BackTraderEngine):
    results =  engine.run()
    res_msg = {'type':'metrics', 'data':[], 'dayReturns':[], 'benchmark':[]} #benchmark基准日收益率
    if engine.params.msg_queen is not None:
        try:
            end_msg = {'type':'msg', 'data':f'当前可用资金:{engine.cerebro.broker.getcash()}, 当前总资产:{engine.cerebro.broker.getvalue()}'}
            engine.params.msg_queen.put(end_msg)
            engine.params.msg_queen.put({'type':'dateIndex','dateIndex':engine.date_index})
            engine.params.msg_queen.put(None)
            if len(results)>0:
                result = results[0]
                if hasattr(result.analyzers, 'DrawDown'):
                    value = result.analyzers.DrawDown.get_analysis()['max']['drawdown'] * (-1)
                    msg = {'name':'最大回撤率', 'value':f"{round(value,2)}%", 'type':'table'}
                    res_msg['data'].append(msg)
                if hasattr(result.analyzers, 'AnnualReturn'):
                    value = result.analyzers.AnnualReturn.get_analysis()
                    value = {k:v for k, v in value.items()}
                    value_msg = []
                    for k,v in value.items():
                        info = f'{k}年: {round(v*100, 2)}%'
                        value_msg.append(info)
                    value_msg = "\n".join(value_msg)
                    msg = {'name':'年度收益率', 'value':value_msg, 'type':'table'}
                    res_msg['data'].append(msg)
                if hasattr(result.analyzers, 'Returns'):
                    value = result.analyzers.Returns.get_analysis()['rnorm100']
                    msg = {'name':'年化收益率（%）', 'value':f"{round(value,2)}%", 'type':'table'}
                    res_msg['data'].append(msg)
                if hasattr(result.analyzers, 'SharpeRatio'):
                    value = result.analyzers.SharpeRatio.get_analysis()['sharperatio']
                    msg = {'name':'年化夏普比率', 'value':f"{round(value,2) if value is not None else 0}%", 'type':'table'}
                    res_msg['data'].append(msg)
                if hasattr(result.analyzers, 'TimeReturn'):
                    value = pd.Series(result.analyzers.TimeReturn.get_analysis())
                    value = list_nan_to_none([round(x*100, 2) if x is not None else None for x in value.to_list()])
                    msg = {'name':'日收益率', 'value':value, 'type':'line'}
                    res_msg['dayReturns'] = msg
                    finally_assest = engine.cerebro.broker.getvalue()
                    msg = {'name':'累计收益', 'value':f"{round((finally_assest-engine.params.cash)*100/engine.params.cash,2)}%", 'type':'table'}
                    res_msg['data'].append(msg)
                    benchmark = pd.Series(result.analyzers.benchmark.get_analysis())
                    benchmark = list_nan_to_none([round(x*100, 2) for x in benchmark.to_list()])
                    res_msg['benchmark'] = benchmark
            engine.params.msg_queen.put(res_msg)
        except Exception as e:
            raise RuntimeError(str(e))
                
    return results


