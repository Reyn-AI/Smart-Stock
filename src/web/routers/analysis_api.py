from fastapi import APIRouter
from pydantic import BaseModel
from src.utils.common import *
from src.utils.stock_utils import *
try:
    import talib
except Exception as e:
    print(e)    
from src.utils.talib_constant import *
from src.utils.registy import CALCULATE_FACTOR_REGISTRY,CALCULATE_FACTOR_REGISTRY_DICT, CLS_REGISTRY_ADDRESS
# from src.backtest.strategys.factors import *
router = APIRouter()

@router.post('/analysis/get_ta_lib_indicator')
async def get_ta_lib_indicator():
    res = {'code':200, 'msg':'请求成功', 'data':[], 'mappingData':{}} #mappingData 返回级联选择器对应的描述 first_second:
    try:
        data = [{'label':'成交量指标',
                 'value':'TALIB_DESC_VOLUME',
                 'children':TALIB_DESC_VOLUME},
                {'label':'形态识别',
                 'value':'TALIB_DESC_PATTERN',
                 'children':TALIB_DESC_PATTERN},
                {'label':'交叉分析指标',
                 'value':'TALIB_DESC_OVERLAP',
                 'children':TALIB_DESC_OVERLAP},
                {'label':'波动指标',
                 'value':'TALIB_DESC_VOLATILITY',
                 'children':TALIB_DESC_VOLATILITY},
                {'label':'动量指标',
                 'value':'TALIB_DESC_MOMENTUM',
                 'children':TALIB_DESC_MOMENTUM},
                {'label':'周期指标',
                 'value':'TALIB_DESC_CYCLE',
                 'children':TALIB_DESC_CYCLE},
                {'label':'统计学指标',
                 'value':'TABLE_DESC_STATISTIC',
                 'children':TABLE_DESC_STATISTIC},
                {'label':'自定义指标',
                 'value':'CALCULATE_FACTOR_REGISTRY',
                 'children':CALCULATE_FACTOR_REGISTRY}]
        res['data'] = data
        for item in TALIB_DESC_VOLUME:
            value = item['value']
            res['mappingData']['TALIB_DESC_VOLUME_'+value] = item['desc']
        for item in TALIB_DESC_PATTERN:
            value = item['value']
            res['mappingData']['TALIB_DESC_PATTERN_'+value] = item['desc']
        for item in TALIB_DESC_OVERLAP:
            value = item['value']
            res['mappingData']['TALIB_DESC_OVERLAP_'+value] = item['desc']
        for item in TALIB_DESC_VOLATILITY:
            value = item['value']
            res['mappingData']['TALIB_DESC_VOLATILITY_'+value] = item['desc']
        for item in TALIB_DESC_MOMENTUM:
            value = item['value']
            res['mappingData']['TALIB_DESC_MOMENTUM_'+value] = item['desc']
        for item in TALIB_DESC_CYCLE:
            value = item['value']
            res['mappingData']['TALIB_DESC_CYCLE_'+value] = item['desc']
        for item in TABLE_DESC_STATISTIC:
            value = item['value']
            res['mappingData']['TABLE_DESC_STATISTIC_'+value] = item['desc']
        for item in CALCULATE_FACTOR_REGISTRY:
            value = item['value']
            res['mappingData']['CALCULATE_FACTOR_REGISTRY_'+value] = item['desc']
            
    except Exception as e:
        print(str(e))
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res

class TALibItem(BaseModel):
    code:str
    funcInfo: dict #指标信息
    startDate:str = None #开始日期
    endDate:str = None #结束日期
    KLineType:str = 'd' #类型

@router.post('/analysis/get_ta_lib_compute')
async def ta_lib_compute(params:TALibItem):
    res = {'code':200, 'msg':'', 'metricData':[], 'rawData':[], 'markPointData':[], 'viewType':None, 'returnName':[]}
    try:
        df = get_day_k_data(code=params.code,
                            start_date=params.startDate,
                            end_date=params.endDate,
                            frequency=params.KLineType,
                            return_list=False)
        rawData = dftodict(df)
        res['rawData'] = rawData
        func_name = params.funcInfo['funcName'] #[listName, funcname]
        func_info = eval(f"{func_name[0]}_DICT.get('{func_name[1]}')")
        res_data = None
        if func_info is not None:
            #处理参数
            params_str = []
            for p in func_info['must_params']:
                # params_str.append(f"{p}=df['{p}']")
                params_str.append(f"df['{p}']")
            if func_info.get('other_params') is not None:
                for p in func_info['other_params']:
                    params_str.append(p)
            params_str = ','.join(params_str)
            if hasattr(talib, func_name[1]):
                expr = f'talib.{func_name[1]}({params_str})'
            else:
                #自定义因子
                expr = f'{func_name[1]}()({params_str})'
                if len(params_str.split(','))>1:
                    params = list(eval(params_str))
                else:
                    params = [eval(params_str)]
                res_data = CLS_REGISTRY_ADDRESS[func_name[1]]()(*params)
            if func_info.get('return'): #函数有多个返回值如布林线
                if res_data is None:
                    res_data = eval(expr)
                res_data = list_nan_to_none(res_data)
                metric_res = {}
                for key, d in zip(func_info.get('return'), res_data):
                    metric_res[key] = d
                res['metricData'] = metric_res
                res['returnName'] = func_info.get('return') #如果多个返回值 返回metricData中key的名字
            else:
                if res_data is None:
                    res_data = eval(expr)
                    if isinstance(res_data, np.ndarray):
                        res_data = res_data.tolist()
                res_data = list_nan_to_none(res_data)
                res['metricData'] = res_data 
            if func_name[0] == 'TALIB_DESC_PATTERN':
                if len(res_data)>0:
                    for i, item in enumerate(res_data):
                        if item!=0:
                            mk_res = {'name':func_name[1],
                                    'value':item,
                                    'xAxis':rawData[i]['date'],
                                    'yAxis':rawData[i]['low']}
                            res['markPointData'].append(mk_res)
            res['viewType'] = func_info.get('view') #可视化的类型 subChart|markPoint|overlap(k线图重叠)
    except Exception as e:
        print(e)
        res['code'] = 500
        res['msg'] = str(e)
    finally:
        return res