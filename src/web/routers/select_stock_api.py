from typing import Dict, List
import json
from pydantic import BaseModel
from src.utils.registy import ANALYSIS_REGISTRY_HISTORY, ANALYSIS_REGISTRY
from src.utils.constant import MARKET_TYPE
from fastapi import APIRouter
from src.engine.engine import Engine
from src.api.tushare_executor import TuShareExecutor
from src.analysis import *
from src.utils.common import get_all_stock_codes
from src.utils.store_util import *
from fastapi import Depends
from src.api.baostock_executor import BaoStockExecutor
from src.utils.registy import CLS_REGISTRY_ADDRESS

router = APIRouter()

class SelectItem(BaseModel):
    """选股web传参
       {
           strategyParams:[{'code':'策略类名', 'params':[{'code':'参数1名','value':参数1值}]}],
           marketParams:[0,1,2,3]
       }
    """
    strategyParams: List = None
    marketParams: List = None

@router.post("/select_stocks/strategy_list")
async def get_strategy_list():
    # 使用加载后的模型进行预测
    res = {'code':200, 'msg':'请求成功', 'data':ANALYSIS_REGISTRY}
    return res

@router.post("/select_stocks/market_list")
async def get_marget_type():
    market_types = [{'code':k, 'name':v} for k,v in MARKET_TYPE.items()]
    res = {'code':200, 'msg':'请求成功', 'data':market_types}
    return res

@router.post("/select_stocks/get_selected_stock_data")
async def get_selected_stock_data(data:SelectItem, store_item=Depends(get_items)):
    uuid_str = get_uuid()
    result = {'code':200, 'msg':'请求成功', 'data':[], 'tabNames':[], 'columns':[], 'uuidStr':uuid_str, 'totalNumbers':[], 'rawData':[]} #总条数
    try:
        strategy_params = data.strategyParams
        marget_params = data.marketParams
        #实例化分析器字符
        analysis_list = []
        for strategy in strategy_params:
            class_name = strategy['code']
            params = strategy.get('paramList', [])
            params_list = [f'market={marget_params}']
            for param in params:
                key = param['code']
                value = param['default']
                params_list.append(f'{key}={value}') 
            params_list = ','.join(params_list)
            analysis_list.append(eval(f"{class_name}({params_list})"))
        engine = Engine(api=TuShareExecutor())
        codes = get_all_stock_codes(market=marget_params)
        # codes = ['600640', '600641']
        params = {
                "ts_code": codes,
                "src": 'sina',
            }
        res = engine.execute(api_name='real_time_data', params=params, analyzer=analysis_list, codes=codes, return_list=False)
        res = {k:list_convert_science_number(v, keys=['流通市值', '总市值', '成交额']) for k,v in res.items()}
        store_item[uuid_str] =res  #存储到缓存用于分页
        result['data'] = {k:[] for k in res.keys()} #分页 此次请求只显示空列表
        result['tabNames'] = return_tab_name(res)
        result['rawData'] = res
        result['columns'] = return_columns(res)
        totalNumbers = [{'name':k, 'numbers':len(v)} for k,v in res.items()]
        result['totalNumbers'] = totalNumbers
    except Exception as e:
        result['code'] = 500
        result['msg'] = str(e)
    finally:
        return result

class IndexItem(BaseModel):
    tabName:str
    uuidStr:str
    currentPage:int #当前页
    pageSize:int #每页数量
    
class UuidItem(BaseModel):
    uuidStr:str

@router.post("/select_stocks/get_selected_stock_data_by_index")
async def get_selected_stock_data_by_index(params:IndexItem, store_item=Depends(get_items)):
    res = {'code':200, 'msg':'请求成功', 'data':[]}
    try:
        res_data = get_by_index(uuid=params.uuidStr,
                                tab_name=params.tabName,
                                start=params.currentPage*params.pageSize,
                                length=params.pageSize,
                                items=store_item)
        
        res['data'] = res_data
    except Exception as e:
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res

@router.post("/select_stocks/delete_cache")
async def del_selected_stock_cache(params:UuidItem):
    """删除缓存的cache"""
    res = {'code':200, 'msg':'删除成功'}
    try:
        flag = delete_cache(params.uuidStr)
        res['msg'] = '删除失败' if not flag else '删除成功'
    except Exception as e:
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res
    
def return_tab_name(data):
    """返回tab name"""
    tab_names = []
    for k in data.keys():
        tab_names.append(k)
    return tab_names

def return_columns(data):
    columns = []
    try:
        for v in data.values():
            if len(v)>0:
                col = list(v[0].keys())
            else:
                col = []
            columns.append(col)
    except Exception as e:
        print(e)
    finally:
        return columns



@router.post("/select_stocks/strategy_list_hisory")
async def get_strategy_list_history():
    # 使用加载后的模型进行预测
    res = {'code':200, 'msg':'请求成功', 'data':ANALYSIS_REGISTRY_HISTORY}
    return res

@router.post("/select_stocks/get_selected_stock_data_by_history")
async def get_selected_stock_data_by_history(data:SelectItem, store_item=Depends(get_items)):
    """根据历史数据选股"""
    uuid_str = get_uuid()
    result = {'code':200, 'msg':'请求成功', 'data':[], 'tabNames':[], 'columns':[], 'uuidStr':uuid_str, 'totalNumbers':[], 'rawData':{}} #总条数
    try:
        strategy_params = data.strategyParams
        marget_params = data.marketParams
        #实例化分析器字符
        analysis_list = []
        for strategy in strategy_params:
            strategy_name = strategy['name']
            class_name = strategy['code']
            params = strategy.get('params', {})
            analysis_list.append({'name':strategy_name, 'instance':CLS_REGISTRY_ADDRESS[class_name](market=marget_params,params=params)})
        res = {}
        for instance in analysis_list:
            name = instance['name']
            cls_func = instance['instance']
            r = await cls_func.analysis()
            if isinstance(r, list):
                res[name] = r
            elif isinstance(r, dict):
                res.update(r)
        store_item[uuid_str] =res  #存储到缓存用于分页
        result['data'] = {k:[] for k in res.keys()} #分页 此次请求只显示空列表
        result['rawData'] = res
        result['tabNames'] = return_tab_name(res)
        result['columns'] = return_columns(res)
        totalNumbers = [{'name':k, 'numbers':len(v)} for k,v in res.items()]
        result['totalNumbers'] = totalNumbers
    except Exception as e:
        result['code'] = 500
        result['msg'] = str(e)
    finally:
        return result